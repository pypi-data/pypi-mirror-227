import numpy as np
import warnings
from bisect import bisect_left, bisect_right
from collections import deque
from typing import Optional
from src.lvdb.timer import store_time
from src.lvdb.lvshard import LVShard
from src.lvdb.profiler import Profiler

class LVInstance:
    """
    Localized Vector Database Instance
    """

    def __init__(self, num_shards: int, max_norm: int, profile: Optional[bool] = False, ttl: Optional[int] = 0, device: Optional[str] = 'cpu'):
        """
        :param num_shards: The number of shards in the database.
        :param profile: Set to true to profile the usage statistics of the database. Disabling it will speed up queries.
        :param ttl: The time to live of caches requests, defined in number of function calls. Defaults to 0 (cache disabled)
        :param device: The device that operations in the database will run on, defaults to cpu.
        """
        super(LVInstance, self).__init__()

        self.__ttl = ttl
        self.__device = device
        self.__num_shards = num_shards
        self.__discretized_norms = np.linspace(0, max_norm, num_shards, endpoint = True)
        self.__shards = {i:LVShard(i, device) for i in range(len(self.__discretized_norms))}
        self.__access_count = [0] * num_shards
        self.__cache_queue = deque()
        self.__cache = {}
        self.profile = profile
        self.profiler = Profiler(num_shards)

        # Each shard has a shard file route to access data from? Loaded using cuPy and cuDf so that it is parallelizable?
        # This provides modular control over embedding data

    @store_time
    def add(self, vector) -> int:
        """
        :param vector: The vector to be added.
        """

        v_norm = np.linalg.norm(vector)
        v_shard = bisect_left(self.__discretized_norms, v_norm)
        self.__shards[v_shard].insert(vector)

        return v_shard

    def batch_add(self, mat):
        """
        :param mat: The matrix of vectors to be added.
        """

        for row in mat:
            self.add(row)

    @store_time
    def delete(self, vector, first: Optional[bool] = True) -> int:
        """
        Deletes a vector, list of vectors, or a matrix of vectors from the database.
        :param vector: The vector to be deleted
        :param first: Set to false to to delete all occurrences of the provided data.
        :return: The shard_id the vector was deleted from
        """

        s_id = bisect_left(self.__discretized_norms, np.linalg.norm(vector))
        self.__shards[s_id].delete(vector, first)

        return s_id

    def batch_delete(self, mat, first: Optional[bool] = True):
        """
        :param mat: The matrix of vectors to be deleted
        :param first: Set to false to delete all occurrences of each row vector in mat
        """

        for row in mat:
            self.delete(row, first)

    @store_time
    def query_norm_range(self, lower_norm: float, upper_norm: float):
        """
        Returns all vectors within the given norm range.
        :param lower_norm: Lower bound for vector norms.
        :param upper_norm: Upper bound for vector norms.
        :return: A list of generators for each shard of vectors within the given range and a list of shards accessed
        """

        l = bisect_left(self.__discretized_norms, lower_norm)
        r = bisect_right(self.__discretized_norms, upper_norm)
        if self.__ttl and (l, r) in self.__cache:
            if self.profile:
                self.profiler.process_cache(True)
            return self.__cache[(l, r)]

        matches = [self.__shards[s_id].get_data(partial = (s_id == l or s_id == r), lo = lower_norm, hi = upper_norm) for s_id in range(l, r + 1)]

        if self.__ttl:
            self.__cache_queue.append((l, r))
            self.__cache[(l, r)] = matches
            if len(self.__cache_queue) > self.__ttl:
                rl, rr =  self.__cache_queue.popleft()
                del self.__cache[(rl, rr)]
            if self.profile:
                self.profiler.process_cache(False)

        return matches, [s_id for s_id in range(l, r + 1)]


    def get_stats(self, times: Optional[bool] = True, plot_times: Optional[bool] = True, cache_utilization: Optional[bool] = False,
                  shard_access: Optional[bool] = False, device_usage: Optional[bool] = False, plot_mem: Optional[bool] = False):
        """
        :param plot_mem: Plot the memory usage over time
        :param plot_times: Plot the add and access times over time
        :param times: Display the average add and access times
        :param cache_utilization: Display the cache hit/miss rate
        :param shard_access: Display a bar plot of the shard access rates
        :param device_usage: Displays a plot of the device usage rates for cpu and gpu
        """

        if not self.profile:
            warnings.warn("You have not enabled profiling. Calling this function does nothing.", Warning)
            return
        if times:
            print(f"Average Insertion Time: {self.profiler.average_add_time()}")
            print(f"Average Access Time: {self.profiler.average_access_time()}")
        if plot_times:
            self.profiler.plot_add_time()
            self.profiler.plot_access_time()
        if cache_utilization:
            hit_ratio, miss_ratio = self.profiler.cache_utilization()
            print(f"Cache Hit Rate: {hit_ratio:.3f}")
            print(f"Cache Miss Rate: {miss_ratio:.3f}")
        if shard_access:
            self.profiler.plot_shard_access_rate()
        if device_usage:
            self.profiler.plot_device_usage()
        if plot_mem:
            self.profiler.plot_mem_usage()
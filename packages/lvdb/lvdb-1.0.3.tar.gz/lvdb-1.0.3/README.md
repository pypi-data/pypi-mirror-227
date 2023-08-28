# LVDB

This is a localized vector database package leveraging Python generators and built-in NumPy text loading to
conserve memory within an environment with resource constraints. It aims to reduce
memory overhead through saving and loading from shard files, in essence
trading runtime for memory.

Usage:
* The entry point for this package is the lvdb.lvinstance.LVInstance class. This can be
imported from lvdb as LVInstance.
* An instance of this class should be initialized and data can be inserted into this instance.
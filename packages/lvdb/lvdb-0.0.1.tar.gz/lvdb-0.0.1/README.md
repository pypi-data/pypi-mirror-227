# Locally Sharded Vector Database

This is a package leveraging Python generators and built-in NumPy text loading to
conserve memory within an environment with resource constraints. It aims to reduce
memory overhead through saving and loading from shard files, in essence
trading runtime for memory. 
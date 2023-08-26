from lvdb import LVInstance
import numpy as np

if __name__ == "__main__":
    lv = LVInstance(5, 15, profile=True)

    lv.get_stats()

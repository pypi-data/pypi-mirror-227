from lvdb import LVDB
import numpy as np

if __name__ == "__main__":
    lv = LVDB.LVInstance(5, 15, profile=True)

    lv.get_stats()

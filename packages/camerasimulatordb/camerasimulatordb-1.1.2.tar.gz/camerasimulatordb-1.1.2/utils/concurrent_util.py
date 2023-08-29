"""This module has a process to call util mymean function one hundred
times with workers.
"""
import concurrent.futures
import time
from util import mymean



def exec_async_mymean():
    """This method call util mymean function one hundred times
    with five workers
    """
    start_time = time.time()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    for _ in range(20):
        executor.submit(mymean)
        executor.submit(mymean)
        executor.submit(mymean)
        executor.submit(mymean)
        executor.submit(mymean)
    print(f"async process take: {(time.time() - start_time)} seconds")

def exec_sync_mymean():
    """This method call util mymean function one hundred times
    without workers
    """
    start_time = time.time()

    for _ in range(100):
        mymean()

    print(f"sync process take: {(time.time() - start_time)} seconds")

if __name__ == "__main__":
    exec_async_mymean()
    exec_sync_mymean()

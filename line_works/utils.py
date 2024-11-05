from time import time


def get_msec() -> int:
    return int(time() * 1000)

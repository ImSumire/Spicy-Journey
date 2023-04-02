from time import perf_counter


def timeit(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print("- %s : \t\t %s" % (func.__name__, round(perf_counter() - start, 6)))
        return result

    return wrapper

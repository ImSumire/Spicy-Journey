# The code  defines a "memoize" function  that  stores the results  of expensive
# calculations  to avoid recalculating  them  each  time  they  are  needed. The
# function  takes  another function  as argument and returns a new function that
# uses a dictionary to store the results.  When  the new function is called with
# arguments, it checks if these arguments are  already present in the  cache. If
# so, it returns the stored result directly. If not,  it calls the function with
# those arguments, stores the result in the cache and returns it.


def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper

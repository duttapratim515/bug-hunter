def bad_func(x, cache={}):
    try:
        cache[x] = x
    except:
        pass
    return cache

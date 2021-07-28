import sys

def command(params: dict, not_found=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            argv = sys.argv

            results = dict()

            for k, v in params.items():
                if k in argv:
                    try:
                        results[k] = argv[argv.index(k)+1]
                    except:
                        results[k] = v
                else:
                    results[k] = not_found

            return func(results, *args, **kwargs)
        return wrapper
    return decorator

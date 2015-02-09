from functools import wraps


class Flag(object):
    def __init__(self, not_enabled_func, config=None):
        self.not_enabled_func = not_enabled_func
        self.config = config if config else lambda: {'DISABLED_FEATURES': []}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ not in self.config()['DISABLED_FEATURES']:
                return func(*args, **kwargs)
            else:
                return self.not_enabled_func(*args, **kwargs)
        return wrapper

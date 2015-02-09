from config import LiveConfig


def feature_enabled(feature_name):
    return feature_name not in LiveConfig.DISABLED_FEATURES


class Flag(object):
    def __init__(self, not_enabled_func):
        self.not_enabled_func = not_enabled_func

    def __call__(self, func):
        if feature_enabled(func.__name__):
            return func
        else:
            return self.not_enabled_func


view_flag = Flag(lambda: ("", 404))

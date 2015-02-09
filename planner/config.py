__all__ = ['LiveConfig']


class Config(object):
    DISABLED_FEATURES = []

    def __init__(self, live_db_path=None):
        self.LIVEDBPATH = live_db_path


# TODO: Decide how to specify which config / env we are in
LiveConfig = Config(live_db_path='sqlite:///live.db')

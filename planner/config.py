__all__ = ['LiveConfig']


class Config(object):
    def __init__(self, live_db_path=None):
        self.LIVEDBPATH = live_db_path


LiveConfig = Config(live_db_path='sqlite:///live.db')

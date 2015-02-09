from os import environ


class StableConfig:
    DBPATH = environ.get("PLANNER_DB", "sqlite:///live.db")
    DISABLED_FEATURES = ['index']


class HeadConfig:
    DBPATH = 'sqlite:///live.db'
    DISABLED_FEATURES = []


CurrentConfig = HeadConfig

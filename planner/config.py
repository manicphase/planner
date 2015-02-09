from os import environ


class StableConfig:
    DBPATH = environ.get("PLANNER_DB", "sqlite:///live.db")
    # TODO: Should these be strings or models/controllers/callables
    DISABLED_FEATURES = ['index', 'schedule', 'add_engagement',
                         'add_client', 'add_contact',
                         'schedule_iteration_for_engagement']


class HeadConfig:
    DBPATH = 'sqlite:///live.db'
    DISABLED_FEATURES = []


CurrentConfig = HeadConfig

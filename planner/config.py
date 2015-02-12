from os import environ
from pkg_resources import resource_filename

db_loc = resource_filename('planner', '../live.db')


class StableConfig:
    DBPATH = environ.get(
        "PLANNER_DB", "sqlite:///{db_loc}".format(db_loc=db_loc)
    )
    # TODO: Should these be strings or models/controllers/callables
    DISABLED_FEATURES = ['index', 'schedule', 'add_engagement',
                         'add_client', 'add_contact',
                         'schedule_iteration_for_engagement']


class HeadConfig:
    DBPATH = "sqlite:///{db_loc}".format(db_loc=db_loc)
    DISABLED_FEATURES = []


CurrentConfig = HeadConfig

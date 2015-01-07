#!/usr/bin/env python

from planner.model import new_live_database, static_live_data


if __name__ == '__main__':
    new_live_database()
    static_live_data()
    print "DB created"

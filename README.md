# Planner
[![Build Status](https://travis-ci.org/saltpy/planner.png)](https://travis-ci.org/saltpy/planner)

Planning tool designed for agile teams working in iterations with third parties

TORG use this tool. You can find TORG at torg.thetestpeople.com.

## Up and Running

### Local Virtual Env Managed by Paver
You will require paver and virtualenv globally in your system Python. On first run use paver once to establish the repo. Then use paver commands as needed. A good place to start is paver ci.

### Using virtualenvwrapper and setup.py
Create a virtualenv as you normally would then install the dependencies then use setup.py develop. You may need to fix things yourself such as changing the virtualenv settings in pavement.py. Do not commit such changes.

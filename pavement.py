import unittest
from os.path import exists

from paver.easy import options, task, needs, sh, Bunch
from paver.runtime import BuildFailure
from paver.setuputils import install_distutils_tasks
from paver.virtual import virtualenv

install_distutils_tasks()

options(
    setup=dict(
        name='Planner',
        version='0.0.0',
        packages=['planner'],
        include_package_data=True,
        author="James Salt",
        author_email="saltpy+planner@gmail.com",
        license="MIT"
    ),
    virtualenv=Bunch(
        packages_to_install=['SQLAlchemy', 'Flask', 'wtforms', 'virtualenv',
                             'flake8', 'ipython', 'coverage'],
        script_name='bootstrap.py',
        dest_dir='venv'
    )
)


@task
@needs(['paver.setuputils.develop', 'db'])
@virtualenv(dir='venv')
def dbrepl():
    """Open ipython with session to live db
    """
    sh('ipython -i scripts/dbrepl.py')


@task
@needs(['minilib', 'generate_setup', 'paver.virtual.bootstrap'])
def once():
    """Run once when you first start using this codebase
    """
    return sh('python bootstrap.py')


@task
@needs(['paver.setuputils.develop'])
@virtualenv(dir="venv")
def unit():
    """Run unit tests
    """
    suite = unittest.TestLoader().discover('test', pattern="_test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.errors == 0 and result.failures == 0:
        raise BuildFailure()


@task
@virtualenv(dir="venv")
def coverage():
    """Run coverage
    """
    sh("coverage erase")
    sh("coverage run --source planner\
       -m unittest discover -s test -p _test_*.py")
    sh("coverage report")


@task
@virtualenv(dir="venv")
def lint():
    """Lint the python files
    """
    return sh('flake8 test planner pavement.py')


@task
@needs(['lint', 'unit'])
@virtualenv(dir="venv")
def ci():
    """Run the continuous integration pipeline
    """
    pass


@task
def clean():
    """Clean up the build artifacts etc
    """
    return max([sh('rm -rf ./*.zip venv bootstrap.py ./*.egg* build'),
                sh('find . -name "*.pyc" -delete')])


@task
@needs(['paver.setuputils.develop'])
@virtualenv(dir="venv")
def db():
    from planner.config import LIVEDBPATH
    if not exists(LIVEDBPATH):
        sh("python scripts/mkdb.py")


@task
@needs(['paver.setuputils.develop', 'ci', 'db'])
@virtualenv(dir="venv")
def up():
    """Start the server up
    """
    return sh("python planner")

import unittest

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
                             'flake8', 'ipython', 'coverage', 'BeautifulSoup'],
        script_name='bootstrap.py',
        dest_dir='venv'
    )
)


@task
@needs(['minilib', 'generate_setup', 'paver.virtual.bootstrap'])
def once():
    """Run once when you first start using this codebase
    """
    return sh('python bootstrap.py')


@task
@needs(['clean', 'paver.setuputils.develop'])
@virtualenv(dir="venv")
def build():
    """Build
    """


@task
@virtualenv(dir="venv")
def unit():
    """Run unit tests
    """
    suite = unittest.TestLoader().discover('test', pattern="_test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.errors or result.failures:
        raise BuildFailure
    return result.errors + result.failures


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
@virtualenv(dir='venv')
def acceptance():
    """Run acceptance tests
    """
    suite = unittest.TestLoader().discover('test', pattern='_acceptance_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.errors or result.failures:
        raise BuildFailure
    return result.errors + result.failures


@task
@needs(['clean', 'build', 'lint', 'unit', 'acceptance'])
@virtualenv(dir="venv")
def ci():
    """Run the continuous integration pipeline
    """
    pass


@task
def clean():
    """Clean up the build artifacts etc
    """
    return max([sh('rm -rf ./*.zip bootstrap.py ./*.egg* build'),
                sh('find . -name "*.pyc" -delete')])


@task
def jsunit():
    """Run javascript unit tests
    """
    return sh("phantomjs scripts/runner.js test/tests.html")


@task
@needs(['build'])
@virtualenv(dir="venv")
def devup():
    """Start the server using HeadConfig
    """
    from planner import config, create_app
    create_app(config.HeadConfig).run(debug=True)


@task
@needs(['paver.setuputils.develop'])
@virtualenv(dir="venv")
def liveup():
    """Start the server up using StableConfig
    """
    from planner import config, create_app
    create_app(config.StableConfig).run()

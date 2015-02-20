import os
import unittest
import fnmatch

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
    pass


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
@needs(['clean', 'build', 'lint', 'jslint', 'unit', 'jsunit', 'acceptance'])
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


def recursive_glob(pattern, *directories):
    matches = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))
    return matches


@task
def jsunit():
    """Run javascript unit tests
    """
    return sh("phantomjs scripts/jstestrunner.js test/tests.html")


@task
def jslint():
    """Run linting on javascript
    """
    files = recursive_glob('*.js', 'scripts', 'planner/static', 'test')
    return sh('phantomjs scripts/jslintrunner.js ' + ' '.join(files))


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

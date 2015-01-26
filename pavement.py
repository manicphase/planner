from paver.easy import task, sh, needs, Bunch, options
from paver.virtual import virtualenv

options(
    setup=dict(
        name='Planner',
        version='0.0.0',
        packages=['planner'],
        include_package_data=True,
        install_requires=['SQLAlchemy', 'Flask', 'wtforms'],
        author="James Salt",
        author_email="saltpy+planner@gmail.com",
        license="MIT",
        tests_require=["virtualenv", "flake8"],
        test_suite="test"
    ),
    virtualenv=Bunch(
        packages_to_install=['SQLAlchemy', 'Flask', 'wtforms', 'virtualenv',
                             'flake8'],
        script_name='bootstrap.py',
        dest_dir='venv'
    )
)


@task
@needs(['paver.virtual.bootstrap'])
def once():
    """Run once when you first start using this codebase
    """
    return sh('python bootstrap.py')


@task
def unit():
    """Run unit tests
    """
    return sh("python -m unittest discover -s test -p _test_*.py")


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
    return max([sh('rm -rf bootstrap.py ./*.egg* build'),
                sh('find . -name "*.pyc" -delete')])

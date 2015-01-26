from paver.easy import task, sh, needs, Bunch, options
from paver.virtual import bootstrap, virtualenv
from paver.setuputils import setup

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
        packages_to_install=['SQLAlchemy', 'Flask', 'wtforms', 'virtualenv', 'flake8'],
        script_name='bootstrap.py',
        dest_dir='venv'
    )
)


@task
def lint():
    return sh('flake8 test planner pavement.py')


@task
@virtualenv(dir="venv")
@needs(['lint', 'test', 'clean'])
def ci():
    """Run the continuous integration pipeline
    """
    pass


@task
def clean():
    first = sh('rm -rf ./*.egg* venv build')
    second = sh('find . -name "*.pyc" -delete')
    return max([first, second])

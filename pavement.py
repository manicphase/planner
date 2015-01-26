from paver.easy import task, sh, needs
from paver.virtual import virtualenv
from paver.setuputils import setup

setup(
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
    sh('rm -rf ./*.egg*')

from paver.easy import task, needs, sh 
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
    tests_require=['flake8', 'virtualenv'],
    test_suite='test'
)

@task
@needs(['flake8', 'test', 'clean'])
def ci():
    """Run the continuous integration pipeline
    """
    pass

@task
def clean():
    sh('rm -rf ./*.egg*')

import re
from setuptools import setup, find_packages


# Read property from project's package init file
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)


setup(
    name='elorating',
    version=get_property('__version__', 'elorating'),
    description='Elo rating system package',
    author='SErAphLi',
    url='https://github.com/Seraphli/elo_rating.git',
    license='MIT License',
    packages=find_packages(),
    install_requires=[
        'tabulate==0.8.2',
        'thrift==0.11.0',
    ]
)

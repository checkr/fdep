from fdep import __VERSION__
from setuptools import setup

setup(
    name="fdep",
    packages=[
        'fdep', 'fdep.backends', 'fdep.commands',
        'fdep.interfaces', 'fdep.servers',
        'fdep.servers.integrations'
    ],
    version=__VERSION__,
    author="Checkr",
    author_email="eng@checkr.com",
    url="http://github.com/checkr/fdep",
    license="MIT LICENSE",
    description="fdep is a framework-agnostic, transport-agnostic, extensible command line tool to shape workflows between machine learning experts and others.",
    long_description="For more details, go to http://github.com/checkr/fdep",
    entry_points={
        'console_scripts': ['fdep=fdep.__main__:main']
    },
    install_requires=[
        'PyYAML==3.10',
        'boto3==1.7.40',
        'requests==2.18.4',
        'colorama==0.3.9',
        'tqdm==4.23.4',
        'json-rpc==1.11.0'
    ]
)

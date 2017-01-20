from setuptools import setup
from fdep import __VERSION__


setup(
    name="fdep",
    packages=['fdep', 'fdep.backends'],
    version=__VERSION__,
    author="Checkr",
    author_email="eng@checkr.com",
    url="http://github.com/checkr/fdep",
    license="MIT LICENSE",
    description="Fdep is a simple, easy-to-use, production-ready tool/library written in Python to download datasets, misc. files for your machine learning projects.",
    long_description="For more details, go to http://github.com/checkr/fdep",
    entry_points={
        'console_scripts': ['fdep=fdep.__main__:main']
    },
    install_requires=[
        'PyYAML==3.12',
        'boto3==1.4.0',
        'requests==2.11.1',
        'colorama==0.3.7',
        'tqdm==4.8.4'
    ]
)

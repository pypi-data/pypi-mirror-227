from setuptools import setup, find_packages

setup(
    name='anonpi',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here
    ],
    entry_points={
        'console_scripts': [
            'myprojectname = anonpi.main:main',
        ],
    },
)

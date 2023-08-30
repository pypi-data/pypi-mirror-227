from setuptools import setup, find_packages

setup(
    name='snugbug',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snugbug=snugbug.main:main',
        ],
    },
)

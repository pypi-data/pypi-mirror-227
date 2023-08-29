from setuptools import setup, find_packages

setup(
    name='snugbug',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        'socketio-client==1.1.0',  # Socket.IO client library
        'datetime',  # Included in Python standard library
        'requests',  # Example dependency
    ],
)

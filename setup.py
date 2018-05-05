from setuptools import setup, find_packages

NAME = "ssocks"
VERSION = "0.1"
setup(
    name = NAME,
    version = VERSION,
    packages = ['ssocks'],
    package_data = {
        "ssocks":["LICENSE"]
    },
    entry_points = {
        'console_scripts': [
            'sslocal = ssocks.sslocal:main',
            'sserver = ssocks.sserver:main'
        ]
    }
)



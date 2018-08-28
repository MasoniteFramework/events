from setuptools import setup

setup(
    name="masonite-events",
    version='1.0.1',
    packages=[
        'events',
        'events.providers',
        'events.commands',
    ],
    install_requires=[],
    include_package_data=True,
)

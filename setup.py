from setuptools import setup

setup(
    name='discord-py-api',
    py_scipts=['discord_py_api'],
    version='2.0.3',
    description='An API written in Python for Discord.',
    author='Lett',
    install_requires=[
        'requests~=2.31.0',
        'maskpass~=0.3.7',
        'setuptools~=68.2.0',
        'websockets~=12.0',
    ],
)

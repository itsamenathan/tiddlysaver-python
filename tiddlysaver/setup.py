from setuptools import setup

setup(
    name='tiddlysaver',
    version='0.1',
    py_modules=['tiddlysaver'],
    install_requires=[
        'click',
        'rotate-backups',
    ],
    entry_points='''
        [console_scripts]
        tiddlysaver=tiddlysaver:http_serve
    ''',
)

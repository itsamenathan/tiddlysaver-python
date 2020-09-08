from setuptools import setup, find_packages

setup(
    name="tiddlysaver",
    version="1.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "flask_autoindex", "gunicorn", "rotate_backups"],
)

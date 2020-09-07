# tiddlysaver-python

[![GitHub last commit](https://img.shields.io/github/last-commit/itsamenathan/tiddlysaver-python)](https://github.com/itsamenathan/tiddlysaver-python) [![Docker Automated build](https://img.shields.io/docker/cloud/automated/itsamenathan/tiddlysaver-python)](https://hub.docker.com/r/itsamenathan/tiddlysaver-python) ![Docker Automated build](https://img.shields.io/docker/image-size/itsamenathan/tiddlysaver-python?sort=semver)

This is a python server for serving and saving tiddlywiki html files.  It will host files from its current direcotry.  It will also save files there as well. 

## Features

* Host tiddlywiki html files.
* Acts as a saver for tiddlywiki html files.
* Creates backups before saving files.
* Removes old backups using [python-rotate-backups](https://github.com/xolox/python-rotate-backups). Backup plan uses the `relaxed` flag.
  * Saves 10 minutely backups
  * Saves 24 hourly backups
  * Saves 30 daily backups
  * Saves 12 monthly backups
  * Saves 7 yearly backups
* Uses [flask](https://flask.palletsprojects.com/) web framework

## Running

### Docker

The image will run tiddlysaver from `/tiddlywiki`.

```
$ docker run -ti --rm 
             -e GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --access-logfile=-" 
             -p 8000:8000 
             -v $PWD/tiddlywiki:/tiddlywiki 
             itsamenathan/tiddlysaver-python:latest
```

### Python

```
$ pip install .
$ gunicorn -b 0.0.0.0:8000  "tiddlysaver:create_app()"
```

## Development

### Running

```
$ pip install -e .
$ export FLASK_APP=tiddlysaver
$ export FLASK_ENV=development
$ flask run --host 0.0.0.0 --port 8000
```

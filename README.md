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

## Running

### Docker

The image will run tiddlysaver from `/tiddlywiki`.

```
$ docker run -ti --rm -v $PWD/tiddlywiki:/tiddlywiki itsamenathan/tiddlysaver-python:latest
```

### Python

```
$ pip install tiddlysaver
$ tiddlysaver --help
```

## Options

### CLI
`-b, --bind ADDRESS` - Specify alternate bind address [default: 127.0.0.0]
`-p, --port INTEGER` - Specify alternate port [default: 8000]

### Environment Variables

`BIND_HOST` - Specify alternate bind address [default: 127.0.0.0]
`BIND_PORT` - Specify alternate port [default: 8000] 

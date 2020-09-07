import datetime
import os
import shutil
import sys

from flask import Flask, request
from flask_autoindex import AutoIndex

import click

import rotate_backups

app = Flask(__name__)


def makebackup(src):
    src = f".{src}"
    (srcpath, srcfile) = os.path.split(src)
    (srcname, src_ext) = os.path.splitext(srcfile)

    now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    backup_dir = f"{srcpath}/backups/{srcname}"
    backup_file = f"{backup_dir}/{srcname}-{now}{src_ext}"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copyfile(src, backup_file)

    return backup_file


def cleanbackups(backup_dir):
    location = rotate_backups.coerce_location(backup_dir)
    backup = rotate_backups.RotateBackups(
        {"minutely": 10, "hourly": 24, "daily": 30, "monthly": 12, "yearly": 7},
        strict=False,
    )
    backup.rotate_backups(location)


@app.route("/<path:file_path>", methods=["OPTIONS"])
def options(file_path): # pylint: disable=unused-argument
    return "", 200, {"dav": "tw5/put"}


@app.route("/<path:file_path>", methods=["PUT"])
def put_file(file_path):
    data = request.get_data()

    # Don't save if we inside a backup directory
    if "backups/" in request.path:
        print("ERROR: Do not save into a backup directory")
        return "Do not save into a backup directory", 403

    backup_file = makebackup(request.path)
    cleanbackups(os.path.dirname(backup_file))
    with open(file_path, "wb") as dst:
        dst.write(data)
    return "OK"


@click.command()
@click.option(
    "-b",
    "--bind",
    default="127.0.0.1",
    envvar="BIND_HOST",
    metavar="ADDRESS",
    help="Specify alternate bind address [default: 127.0.0.0]",
)
@click.option(
    "-p",
    "--port",
    default=8000,
    envvar="BIND_PORT",
    help="Specify alternate port [default: 8000]",
)
def http_serve(bind, port):
  """Script to serve a tiddlywiki saver."""
  # AutoIndex takes care of GET routes on / and /<path:file_path>
  AutoIndex(app, browse_root=os.path.curdir)
  app.run(host=bind, port=port)

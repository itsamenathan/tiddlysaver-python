#!/usr/bin/env python3

import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import shutil
import sys

import click

import rotate_backups

class httpdHandler(SimpleHTTPRequestHandler):
    def makebackup(self, src):
        (srcpath, srcfile) = os.path.split(src)
        (srcname, src_ext) = os.path.splitext(srcfile)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_dir = f"{srcpath}/backups/{srcname}"
        backup_file = f"{backup_dir}/{srcname}-{now}{src_ext}"

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        shutil.copyfile(src, backup_file)

        self.cleanbackups(backup_dir)

    def cleanbackups(self, backup_dir):
        location = rotate_backups.coerce_location(backup_dir)
        backup = rotate_backups.RotateBackups(
            {"minutely": 10,
             "hourly": 24,
             "daily": 30,
             "monthly": 12,
             "yearly": 7},
            strict=False,
        )
        backup.rotate_backups(location)

    def do_PUT(self):
        length = int(self.headers["Content-Length"])
        path = self.translate_path(self.path)

        # Don't save if we inside a backup directory
        if "/backups/" in path:
            print("ERROR: Do not save into a backup directory")
            self.send_response(403)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return

        # Make a backup, clean old backups, and overwrite current file
        self.makebackup(path)
        with open(path, "wb") as dst:
            dst.write(self.rfile.read(length))

        # Return 200
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("allow", "GET,HEAD,POST,OPTIONS,CONNECT,PUT,DAV,dav")
        self.send_header("x-api-access-type", "file")
        self.send_header("dav", "tw5/put")
        self.end_headers()


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
    httpd = HTTPServer((bind, port), httpdHandler)
    print(f"Serving HTTP on {bind} port {port} (http://{bind}:{port}/) ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)

""" python server for serving and saving tiddlywiki html """
import datetime
import os
import shutil

from flask import Flask, request  # pylint: disable=import-error
from flask_autoindex import AutoIndex  # pylint: disable=import-error

import rotate_backups  # pylint: disable=import-error


def create_app():
    """ Create Flask app """
    app = Flask(__name__)

    def makebackup(src):
        app.logger.info("Making Backups")
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
        app.logger.info("Cleaning Backups")
        location = rotate_backups.coerce_location(backup_dir)
        backup = rotate_backups.RotateBackups(
            {"minutely": 10, "hourly": 24, "daily": 30, "monthly": 12, "yearly": 7},
            strict=False,
        )
        backup.rotate_backups(location)

    @app.route("/<path:file_path>", methods=["OPTIONS"])
    def _options(file_path):  # pylint: disable=unused-argument
        app.logger.info("Received OPTIONS")
        return "", 200, {"dav": "tw5/put"}

    @app.route("/<path:file_path>", methods=["PUT"])
    def _put_file(file_path):
        app.logger.info("Received PUT")

        data = request.get_data()

        # Don't save if we inside a backup directory
        if "backups/" in request.path:
            app.logger.warning("Do not save into a backup directory")
            return "Do not save into a backup directory", 403

        backup_file = makebackup(request.path)
        cleanbackups(os.path.dirname(backup_file))
        with open(file_path, "wb") as dst:
            dst.write(data)
        return "OK"

    AutoIndex(app, browse_root=os.path.curdir)

    return app

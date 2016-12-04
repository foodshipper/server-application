import logging
import os
import sys

from crontab import CronTab
from flask import Flask

from ean.api import api
from ean.database import check_db


def check_cronjob():
    logging.debug("Checking for Cronjob")

    try:
        my_cron = CronTab(user=True)

        cmd = "DB_HOST='" + os.environ.get("DB_HOST", "localhost") + "' "
        cmd += "DB_USER='" + os.environ.get("DB_USER", "foodship") + "' "
        cmd += "DB_PASS='" + os.environ.get("DB_PASS", "") + "' "
        cmd += "DB_NAME='" + os.environ.get("DB_NAME", "foodship") + "' "
        cmd += sys.executable + " " + os.getcwd() + "/ean/cron/cron.py"

        i = 0
        for job in my_cron.find_command(cmd):
            i += 1
            logging.info("Cronjob does already exist: " + str(job))
            return True

        job = my_cron.new(cmd, 'Foodship API Worker')
        job.minute.every(15)
        my_cron.write()
        logging.info("Wrote Crontab")
    except FileNotFoundError:
        logging.warning("Could not create Crontab Entry: File not found")


def create_app():
    logging.basicConfig(filename='foodship.log', level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.debug("Creating App")
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    api.init_app(app)
    check_db()
    check_cronjob()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

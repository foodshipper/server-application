from flask import Flask
from crontab import CronTab
import sys, os
from ean.api import api
from ean.database import check_db


def check_cronjob():
    print("Checking for Cronjob")
    try:
        my_cron = CronTab(user=True)
        cmd = sys.executable + " " + os.getcwd() + "/cron/cron.py"
        if my_cron.find_command(cmd) is not None:
            print("Cronjob does already exist")
            return True

        job = my_cron.new(cmd, 'Foodship API Worker')
        job.minute.every(15)
        my_cron.write()
        print("Wrote Crontab")
    except FileNotFoundError:
        print("Could not create Crontab Entry: File not found", file=sys.stderr)


def create_app():
    print("Creating App")
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    api.init_app(app)
    check_db()
    check_cronjob()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

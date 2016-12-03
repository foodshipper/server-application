from flask import Flask
from crontab import CronTab
import sys, os
from ean.api import api
from ean.database import create_tables


def check_cronjob():
    try:
        my_cron = CronTab(user=True)
        cmd = sys.executable + " " + os.getcwd() + "/cron/cron.py"
        if my_cron.find_command(cmd) is not None:
            return True

        job = my_cron.new(cmd, 'Foodship API Worker')
        job.minute.every(15)
        my_cron.write()
        print("Wrote Crontab")
    except FileNotFoundError:
        print("Could not create Crontab Entry: File not found", file=sys.stderr)


def create_app():
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    api.init_app(app)
    create_tables()
    check_cronjob()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

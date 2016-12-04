import sys

from ean.app import create_app
from werkzeug.contrib.fixers import ProxyFix # needed for http server proxies
from werkzeug.debug import DebuggedApplication
import logging

app = create_app()
logging.debug("Use Python Version " + str(sys.version_info.major))
app.wsgi_app = ProxyFix(app.wsgi_app) # needed for http server proxies
application = DebuggedApplication(app, True)
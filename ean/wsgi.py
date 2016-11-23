import sys

from ean.app import create_app
from werkzeug.contrib.fixers import ProxyFix # needed for http server proxies
from werkzeug.debug import DebuggedApplication

print("Use Python Version " + sys.version_info)
app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app) # needed for http server proxies
application = DebuggedApplication(app, True)
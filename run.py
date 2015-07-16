#!/usr/bin/env python
from app import app
from config import PRODUCTION, APP_HOST, APP_PORT

if PRODUCTION:
    app.run(host=APP_HOST, port=APP_PORT, debug=False, threaded=True, use_reloader=True, reloader_interval=60)
else:
    app.run(host=APP_HOST, port=APP_PORT, debug=True, use_reloader=True, reloader_interval=1)

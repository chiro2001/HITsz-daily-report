import os
from flask import Flask
from reporter.utils import logger
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app import app as app_main

app_new = Flask(__name__)

# 中间件
dm = DispatcherMiddleware(app_new, {
    '/release', app_main
})

if __name__ == '__main__':
    run_simple('0.0.0.0', int(os.environ.get("PORT", '8081')), dm, use_reloader=False)

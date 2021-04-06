import json
import requests
import datetime
from flask import *
from flask_cors import CORS
from reporter.make_result import make_result
from reporter.config import config
from reporter.utils import logger, handle_request_exceptions
from tasks import epidemic_report

app_name = 'epidemic'
app = Flask(app_name)
CORS(app, supports_credentials=True)
handle_request_exceptions(app)


def get_apis() -> dict:
    return {
        '/': {
            "description": 'Index and description of the Epidemic Report API',
            'methods': ['GET'],
            'args': {},
            'rets': {
                'apis': "Lists of API urls and args"
            }
        },
        '/report': {
            "description": 'HITsz疫情上报',
            'methods': ['GET', 'POST'],
            'args': {
                "username": {
                    "description": 'HITsz SSO登录用户名（学号）',
                    "required": True
                },
                "password": {
                    "defscription": "HITsz SSO登录密码",
                    "required": True
                },
                "api_key": {
                    "description": "Server酱的SCKEY",
                    "required": False
                }
            }
        }
    }


@app.route('/', methods=['GET'])
def index():
    return make_result(data={
        'description': f'HItsz-daily-reporter API v{config.data.get("epidemic-report-version", None)}',
        'apis': get_apis()
    })


@app.route('/report/', methods=['GET', 'POST'])
def report():
    if request.method == 'GET':
        args = request.args
    elif request.method == 'POST':
        try:
            args = request.json
        except json.decoder.JSONDecodeError:
            return make_result(400)
    else:
        return make_result(400)
    args = json.loads(json.dumps(args))
    required = ['username', 'password']
    for r in required:
        if r not in args:
            return make_result(400, message=f'Arg {r} is required')
    is_successful, msg = epidemic_report.main(args)
    if is_successful:
        txt = f"疫情上报成功！{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        txt = f"疫情上报失败，原因：{msg}{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
    if 'api_key' in args and not is_successful:
        requests.get(f"https://sc.ftqq.com/{args.api_key}.send?text={txt}")
    return make_result(code=200 if is_successful else 403, message=txt)

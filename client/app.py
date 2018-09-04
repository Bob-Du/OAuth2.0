from flask import Flask, url_for, redirect, render_template, request
from urllib import parse
import requests
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login-third-party')
def login_third_party():
    params = {
        'response_type': 'code',  # 授权类型,授权码模式固定为'code'
        'client_id': '测试客户端',  # 客户端ID,此处为简化测试,直接使用客户端名称
        'redirect_uri': 'http://127.0.0.1:4000/get-token',  # 授权服务器重定向URI
        'scope': 'all',  # 申请的权限范围
        'state': 'logining',  # 客户端当前状态,授权服务器应原样返回
    }
    return redirect('http://127.0.0.1:5000/authorization-login?' + parse.urlencode(params))


@app.route('/get-token')
def get_token():
    """client通过授权服务器将用户浏览器重定向到此时携带的授权码code向授权服务器请求token"""
    code = request.args['code']  # 授权码
    print('发起请求授权码是' + code)
    token = get_token_by_code(code)
    return '授权令牌是' + token


def get_token_by_code(code):
    params = {
        'grant_type': 'authorization_code',  # 表示授权码模式,固定值
        'code': code,  # 授权码
        'redirect_uri': 'http://127.0.0.1:4000/get-token',  # 必须和前面相同的重定向URI
        'client_id': '测试客户端',
    }
    response = requests.get('http://127.0.0.1:5000/token', params)
    # 这里特别慢 且极不稳定 不知道是不是因为运行在开发环境没有正规的web服务器的原因
    token = json.loads(response.text)['access_token']
    return token


if __name__ == '__main__':
    app.run(port=4000, debug=True)

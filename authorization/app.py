from flask import Flask, render_template, request, redirect, jsonify
from urllib import parse

app = Flask(__name__)


@app.route(r'/authorization-login', methods=['GET', 'POST'])
def authorization_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # 测试用账号密码,就不连接数据库实际验证了
        if request.form['username'] == 'name' and request.form['password'] == 'mima':
            # 登录成功 返回授权码
            redirect_uri = request.args['redirect_uri']
            params = {
                'code': 1111,  # 授权码,只能使用一次,通常10分钟过期,测试简化为固定值
                'state': request.args['state'],  # 原样返回客户端请求时携带的该参数
            }
            return redirect(redirect_uri + '?' + parse.urlencode(params))
        else:
            return '<script>alert("账号或密码错误");location.href="' + request.url + '"</script>'


@app.route(r'/token')
def token():
    if request.args['code'] == '1111':
        # 确认授权码和重定向URI无误后发放令牌
        params = {
            'access_token': 'my_token',  # 发放的令牌
            'token_type': 'bearer',  # 令牌类型,必选 bearer或mac
            'expires_in': '10000',  # 过期时间,单位为秒
            'refresh_token': 'my_refresh_token',  # 更新令牌时获取下一次访问令牌用
            'scope': 'all',  # 权限范围
        }
        return jsonify(params)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

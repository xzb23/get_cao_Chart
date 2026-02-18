from package import *
import data_io

app = flask.Flask(__name__)

@app.route('/api/getcao')
def give_user():
    uid = flask.request.args.get('uid')
    count = data_io.get_user_count(uid)
    print(uid, count)
    if count == -1: # -1保留，当管理员手动设置count=-1时，用户无法被cao
        re_text = "err:\t未查询到用户"
    else:
        data_io.give_user(uid)
        re_text = "ok"
    return flask.redirect(flask.url_for('get_users_cao'))

@app.route('/')
def get_users_cao():
    users = data_io.get_all_users()
    return flask.render_template('index.html', users=users)


@app.route('/admin')
def admin():
    password = flask.request.cookies.get("key")
    if not password:
        return flask.redirect(flask.url_for('login'))
    users = data_io.get_all_users()
    return flask.render_template('admin.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    password = flask.request.cookies.get("key")
    uid = flask.request.form.get('name')
    description = flask.request.form.get('description')
    if data_io.add_user(uid, description, password):
        re_text = "ok"
    else:
        re_text = "err:\t用户已存在"
    return flask.redirect(flask.url_for('admin'))

@app.route('/delete_user/<uid>', methods=['GET', 'POST'])
def delete_user(uid):
    password = flask.request.cookies.get("key")
    data_io.delete_user(uid, password)
    return flask.redirect(flask.url_for('admin'))

@app.route('/update_user/<uid>', methods=['GET', 'POST'])
def update_user(uid):
    name_new = flask.request.form.get('name')
    count = flask.request.form.get('count')
    description = flask.request.form.get('description')
    password = flask.request.cookies.get("key")
    data_io.update_user(uid, name_new, count, description, password)
    return flask.redirect(flask.url_for('admin'))

@app.route('/login/check', methods=['GET', 'POST'])
def check():
    password = flask.request.form.get('password')
    if password:
        resp = flask.make_response("ok, <a href='/admin'>返回管理页面</a>") 
        resp.set_cookie("key", password, max_age=3600)
        return resp
    else:
        return "err", 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    return flask.render_template('login.html')

def run(host:str, port:int):
    app.run(host, port, debug=False)
    return
# -*- coding: utf-8 -*-
from database.groups import Groups
from database.users import User
from database.files import Files
from app import app
from app.__init__ import db_sess

from os.path import join as join_path

from flask import redirect, render_template, send_file, request as flask_request


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@app.route('/profile/<nickname>')
def profile(nickname=None):
    current_sess = db_sess.create_session()
    if not nickname:
        '''nickname = login_from_github'''
        nickname = 'obeyurfate'
    print(nickname)
    image = '../static/images/profile.png'
    user = current_sess.query(User).filter(User.nickname == nickname).first()
    print(user.groups)
    context = {'image': image,
               'groups': user.groups,
               'nickname': nickname,
               'description': user.description
               }
    return render_template('profile.html', **context)


@app.route('/redirect/<page>', methods=['POST', 'GET'])
def redirect(page):
    return redirect(page)


@app.route('/favicon.ico')
def favicon():
    path = join_path('/', app.root_path, 'static'
                     ).replace('\\', '/')
    current_sess = db_sess.create_session()
    files = current_sess.query(Files).filter(Files.name == 'favicon').first()
    return send_file(path + '/' + files.path)


@app.route('/find_user')
def group_finder():
    current_sess = db_sess.create_session()
    result = []
    search_text = flask_request.args.get("search", default='')
    if search_text != '':
        result = current_sess.query(User).filter(User.nickname == search_text)
        result = [[user.nickname, user.description] for user in result]
    context = {
        'search_text': search_text,
        'result': result
    }
    return render_template('user_finder.html', params=context)


@app.route('/ide')
def ide():
    return render_template('ide.html')


@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('404.html', e=error), 404


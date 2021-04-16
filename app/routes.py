# -*- coding: utf-8 -*-
from database.groups import Groups
from database.users import User
from database.files import Files
from app.__init__ import db_sess

from os.path import join as join_path

from flask import redirect, render_template, send_file, request as flask_request
from app import app


@app.route('/profile')
def index():
    current_sess = db_sess.create_session()
    '''image = image_url_from_github'''
    '''nickname = login_from_github'''
    nickname = 'nickname'
    image = '../../static/profile.png'
    groups = current_sess.query(Groups)
    context = {'image': image,
               'groups': groups,
               'nickname': nickname,
               }
    return render_template('profile.html', **context)


@app.route('/redirect/<page>', methods=['POST', 'GET'])
def redirect(page):
    return redirect(page)


@app.route('/favicon.ico')
def favicon():
    path = join_path('/', app.root_path, 'static')
    current_sess = db_sess.create_session()
    files = current_sess.query(Files).filter(Files.name == 'favicon')
    return send_file(path, files)


@app.route('/find_groups')
def group_finder():
    current_sess = db_sess.create_session()
    result = []
    search_text = flask_request.args.get("search", default='')
    if search_text != '':
        result = current_sess.query(Groups).filter(Groups.id == id)
        result = [[group.id, group.description] for group in result]
    context = {
        'search_text': search_text,
        'result': result
    }
    return render_template('group_finder.html', params=context)


@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('404.html', e=error), 404



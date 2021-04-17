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
    return render_template('base.html')


@app.route('/profile')
def profile():
    current_sess = db_sess.create_session()
    '''image = image_url_from_github'''
    '''nickname = login_from_github'''
    nickname = 'nickname'
    image = '../static/images/profile.png'
    groups = current_sess.query(Groups).all()
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
    return send_file('static/images/favicon.ico')


@ app.route('/find_groups')
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

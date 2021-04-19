# -*- coding: utf-8 -*-
from database.groups import Groups

from flask import redirect, render_template
from flask import request as flask_request
from flask import send_file, url_for, session

from requests_oauthlib import OAuth2Session

from app import *
from app.__init__ import db_sess


@app.route('/')
def index():
    # Main page
    return render_template('base.html')


@app.route('/login')
def login():
    # Login using OAuth
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(
        authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/favicon.ico')
def favicon():
    # Returning favicon
    return send_file('static/images/favicon.ico')


@app.errorhandler(Exception)
def handle_exception(error):
    # Handle all exceptions
    return render_template('404.html', e=error), 404


@app.route('/group/<name>')
def group(name):
    current_sess = db_sess.create_session()
    group = [group for group in current_sess.query(Groups).all()
             if name == group.name][0]
    result = {
        'name': group.name,
        'description': group.description,
        'users': group.users.split(','),
        'link': group.github,
        'icon': group.icon
    }
    for key in result:
        if result[key] is None:
            result[key] = ''
    context = {'description': result[1],
               'link': result[-2],
               'users': result[-3],
               'name': result[0],
               'icon': result[-1]
               }
    return render_template('group.html', **context)


@app.route('/create_group', methods=['POST', 'GET'])
def create_group():
    if flask_request.method == 'POST':
        current_sess = db_sess.create_session()
        name = flask_request.form['name']
        icon = flask_request.form['icon']
        description = flask_request.form['description']
        group = Groups(name=name, description=description, icon=icon)
        current_sess.add(group)
        current_sess.commit()
        return redirect('/group/' + name)
    return render_template('create_group.html')


@app.route('/find_groups')
def group_finder():
    result = []
    current_sess = db_sess.create_session()
    search_text = flask_request.args.get('search', default='')
    if search_text != '':
        result = current_sess.query(Groups).all()
        result = [[group.name, group.description] for group in result
                  if search_text in group.name]
    context = {
        'search_text': search_text,
        'result': result
    }
    return render_template('group_finder.html', **context)


@app.route('/callback')
def get_callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.profile'))


@app.route('/profile')
def profile():
    current_sess = db_sess.create_session()
    groups = current_sess.query(Groups).all()
    '''
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())
    image = image_url_from_github
    nickname = login_from_github
    print(jsonify(github.get('https://api.github.com/user').json()))
    '''
    nickname = 'nickname'
    image = '../static/images/profile.png'

    context = {
        'image': image,
        'groups': groups,
        'nickname': nickname,
    }

    return render_template('profile.html', **context)


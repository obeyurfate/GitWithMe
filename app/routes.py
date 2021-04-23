# -*- coding: utf-8 -*-
from database.temps import Temps
from database.users import User
from database.groups import Groups
from app import *

from contextlib import redirect_stdout
from flask import redirect, render_template, send_file, request as flask_request, request
from flask import url_for, session
import io
from requests_oauthlib import OAuth2Session
import runpy


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    # Login using OAuth
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(
        authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/profile')
@app.route('/profile/<nickname>')
def profile(nickname=None):
    current_sess = db_sess.create_session()
    if not nickname:
        '''nickname = login_from_github'''
        nickname = 'obeyurfate'
    '''
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())
    image = image_url_from_github
    nickname = login_from_github
    print(jsonify(github.get('https://api.github.com/user').json()))
    '''
    image = '../static/images/profile.png'
    user = current_sess.query(User).filter(User.nickname == nickname).first()
    context = {'image': image,
               'groups': user.groups,
               'nickname': nickname,
               'description': user.description
               }
    return render_template('profile.html', **context)


@app.route('/group/<name>')
def group(name):
    current_sess = db_sess.create_session()
    group = current_sess.query(Groups).filter(name == Groups.name).first()
    result = {
        'name': group.name,
        'description': group.description,
        'users': group.user,
        'link': group.github,
        'icon': group.icon
    }
    for key in result:
        if result[key] is None:
            result[key] = ''
    context = {'description': result['description'],
               'link': result['link'],
               'users': result['users'],
               'name': result['name'],
               'icon': result['icon']
               }
    return render_template('group.html', **context)


@app.route('/favicon.ico')
def favicon():
    # Returning favicon
    return send_file('static/images/favicon.ico')


@app.route('/find_user')
def user_finder():
    current_sess = db_sess.create_session()
    search_text = flask_request.args.get("search", default='')
    if search_text != '':
        users = current_sess.query(User).filter(User.nickname == search_text)
        users = [[user.nickname, user.description] for user in users]
        return render_template('user_finder.html', users=users, search_text=search_text)
    else:
        return render_template('user_finder.html', search_text=search_text)


@app.route('/create_group', methods=['POST', 'GET'])
def create_group():
    if flask_request.method == 'POST':
        current_sess = db_sess.create_session()
        name = flask_request.form['name']
        icon = flask_request.form['icon']
        description = flask_request.form['description']
        group = Groups(name=name,
                       description=description,
                       icon=icon)
        current_sess.add(group)
        current_sess.commit()
        return redirect('/group/' + name)
    return render_template('create_group.html')


'''@app.errorhandler(Exception)
def handle_exception(error):
    # Handle all exceptions
    return render_template('404.html', e=error), 404
'''

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


@app.route('/ide', methods=['GET', 'POST'])
def ide():
    current_sess = db_sess.create_session()
    nickname = 'obeyurfate'
    user = current_sess.query(User).filter(User.nickname == nickname).first()
    if request.method == 'POST':
        code = '\n'.join(request.form['code'].split('<br/>'))
        code = code.rstrip('\n')
        if not request.form['save']:
            try:
                with open('TEMP.py', 'w', encoding='utf-8') as temp_file:
                    temp_file.write(code)
                temp_f = current_sess.query(Temps).filter(
                    Temps.user_id == user.id).first()
                temp_f.code = code
                f = io.StringIO()
                with redirect_stdout(f):
                    runpy.run_path('TEMP.py')
                s = f.getvalue()
                result = s
                context = {
                    'code': code,
                    'result': result
                }
                return render_template('ide.html', **context)
            except Exception as e:
                result = e
                context = {
                    'code': code,
                    'result': result
                }
                return render_template('ide.html', **context)
        else:
            id = user.id
            temp_f = current_sess.query(Temps).filter(
                Temps.user_id == id).first()
            print(temp_f)
            if temp_f:
                temp_f.code = code
                current_sess.merge(temp_f)
                current_sess.commit()
            else:
                temp_f = Temps(code=code, user_id=id)
                current_sess.add(temp_f)
                current_sess.commit()
            return render_template('ide.html', code=code)

    elif request.method == 'GET':
        code = ''
        temp_f = current_sess.query(Temps).filter(
            Temps.user_id == user.id).first()
        if temp_f:
            code = temp_f.code
        return render_template('ide.html', code=code, result="")

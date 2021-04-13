from flask import Flask
from flask import render_template
from dotenv import load_dotenv
import os

from database import db_sess
from database.groups import Groups

app = Flask(__name__)
load_dotenv('.env')


@app.route('/profile')
def index():
    db_session = db_sess.create_session()
    '''image = image_url_from_github'''
    '''nickname = login_from_github'''
    nickname = 'nickname'
    image = 'static/profile.png'
    groups = db_session.query(Groups)
    context = {'image': image,
               'groups': groups,
               'nickname': nickname,
               }
    return render_template('profile.html', **context)


if __name__ == '__main__':
    db_sess.global_init(os.getenv("database"))
    app.run(port=8000, host='localhost')

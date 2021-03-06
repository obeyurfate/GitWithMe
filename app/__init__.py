# -*- coding: utf-8 -*-
import os
from os import getenv, urandom, environ

from database import db_sess
from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__, template_folder='./templates')
load_dotenv('.env')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_id = environ.get('client_id')
client_secret = environ.get('client_secret')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from app import routes

app.secret_key = urandom(24)
db_sess.global_init('database/db.db')

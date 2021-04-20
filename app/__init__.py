# -*- coding: utf-8 -*-

from os import urandom

from database import db_sess
from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__, template_folder='./templates')
load_dotenv('.env')

database = "database/db.db"
client_id = "9ff8f300ec3d64d48796"
client_secret = "9e023423bc80ab40892da67823c24463487e7293"
secret_key = "QWRWLIWDTDBDEFJACZEBYQEBQPUPZVVHUNSN"
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from app import routes

app.secret_key = urandom(24)
db_sess.global_init('database/db.db')

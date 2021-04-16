# -*- coding: utf-8 -*-

from database import db_sess

from os import urandom, getenv
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__, template_folder='./templates/')
load_dotenv('.env')

from app import routes

app.secret_key = urandom(24)
db_sess.global_init(getenv("database"))
app.run()

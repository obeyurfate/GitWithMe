# -*- coding: utf-8 -*-

from os import urandom

from flask import Flask

app = Flask(__name__, template_folder='./templates/')

from app import routes

app.secret_key = urandom(24)
app.run()

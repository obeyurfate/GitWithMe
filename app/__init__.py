from flask import Flask
from os import environ, urandom

app = Flask(__name__, template_folder='./templates/')
from app import routes


environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = urandom(24)
app.run(debug=True)

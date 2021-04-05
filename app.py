from requests_oauthlib import OAuth2Session

import dotenv
import os
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
from flask_classful import FlaskView, route


app = Flask(__name__)
dotenv.load_dotenv()


class AuthenticationView(FlaskView):
    def __init__(self):
        self.client_id = os.environ.get('client_id')
        self.client_secret = os.environ.get('client_secret')
        self.authorization_base_url = 'https://github.com/login/oauth/authorize'
        self.token_url = 'https://github.com/login/oauth/access_token'

    def index(self):
        github = OAuth2Session(self.client_id)
        authorization_url, state = github.authorization_url(self.authorization_base_url)

        session['oauth_state'] = state
        return redirect(authorization_url)

    @route('/callback')
    def get_callback(self):
        github = OAuth2Session(self.client_id, state=session['oauth_state'])
        token = github.fetch_token(self.token_url, client_secret=self.client_secret,
                                   authorization_response=request.url)

        session['oauth_token'] = token

        return redirect(url_for('.profile'))

    @route("/profile", methods=["GET"])
    def profile(self):
        github = OAuth2Session(self.client_id, token=session['oauth_token'])
        print(jsonify(github.get('https://api.github.com/user').json()))
        return jsonify(github.get('https://api.github.com/user').json())


AuthenticationView.register(app)


if __name__ == '__main__':
    # позволяет использовать простой callback HTTP
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run()

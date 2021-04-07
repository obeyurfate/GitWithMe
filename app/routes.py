from flask import render_template
from .tools import Pages
from app import app

pages = Pages()


@app.route('/error')
def error():
    return render_template(pages.get_page('error'))

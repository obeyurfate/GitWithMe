# -*- coding: utf-8 -*-

from os.path import join as join_path

from flask import redirect, render_template, send_file

from app import app

from .tools import Files, Pages

pages = Pages()
files = Files()


@app.route('/error')
def error():
    return render_template(pages.get_page('error'))


@app.route('/redirect/<page>', methods=['POST', 'GET'])
def redirect(page):
    return redirect(page)


@app.route('/favicon.ico')
def favicon():
    path = join_path('/', app.root_path, 'static'
                     ).replace('\\', '/') + files.get_file('favicon')
    return send_file(path,
                     files.get_file('favicon'))


@app.errorhandler(Exception)
def handle_exception(error):
    return render_template(pages.get_page('error'), e=error), 404


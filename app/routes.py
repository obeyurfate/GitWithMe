# -*- coding: utf-8 -*-

from os.path import join as join_path

from flask import redirect, render_template, send_file, request as flask_request

from app import app

from .tools import DataBase

pages = [DataBase(), ['html', 'pages']]
files = [DataBase(), ['path', 'files']]
groups = [DataBase(), ['name, description', 'groups']]


@app.route('/redirect/<page>', methods=['POST', 'GET'])
def redirect(page):
    return redirect(page)


@app.route('/favicon.ico')
def favicon():
    path = join_path('/', app.root_path, 'static'
                     ).replace('\\', '/') + pages[0].get(*pages[1], 'error')
    return send_file(path,
                     files[0].get(*files[1], 'favicon'))


@app.route('/find_groups')
def group_finder():
    result = []
    search_text = flask_request.args.get("search", default='')
    if search_text != '':
        result = groups[0].get(*groups[1], search_text, False)
        result = [[group[0], group[1]] for group in result]
    print(result)
    return render_template(
        pages[0].get(*pages[1], 'group_finder'),
        search_text=search_text,
        result=result
    )


@ app.errorhandler(Exception)
def handle_exception(error):
    return render_template(pages[0].get(*pages[1], 'error'), e=error), 404



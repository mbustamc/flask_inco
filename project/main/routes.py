from flask import render_template, redirect, url_for

from flask import request, jsonify

from project.main import bp


@bp.route("/")
def index():
    return redirect(url_for('task.list'))


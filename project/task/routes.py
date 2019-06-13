from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
import flask_excel as excel


import json

from project.task import bp
from project import db

from project.models import *

from .forms import TaskForm

@bp.route('/')
#@login_required
def list():
    tasks = Task.query.all()
    return render_template('task/list.html', tasks=tasks)


@bp.route('/task', methods=['POST', 'GET'])
@login_required
def add_task():
    title = "Add TaskForm"
    form = TaskForm()

    
    if form.validate_on_submit():
        content = request.form.get('content')
        task = Task(content)
        task.area = form.area.data
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task.list'))
    return render_template('task/task.html', title=title, form=form)


@bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for('task.list'))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('task.list'))


@bp.route('/modify/<int:task_id>', methods=['GET', 'POST'])
@login_required
def modify_task(task_id):
    title='Actualiza tarea'
    task = Task.query.get(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.content = form.content.data
        task.area = form.area.data
        task.modify = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('task.list'))
    elif request.method == 'GET':
        #form.populate_obj(task)
        form.content.data = task.content
        form.area.data = task.area
    return render_template('task/modify_task.html', title=title, task=task,
        form=form)


@bp.route('/done/<int:task_id>')
@login_required
def done_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect(url_for('task.list'))

    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect(url_for('task.list'))


"""
@bp.route("/export")
def export():
    tasks = Task.query.all()
    return jsonify(data=[task.serialize for task in tasks])
    #return jsonify(all_args)
"""

@bp.route("/import", methods=['GET', 'POST'])
def do_import():
    if request.method == 'POST':
        def task_init_func(row):
            p = Task(row['content'], row['done'])
            return p
        request.save_book_to_database(field_name='file', session=db.session,
                                      tables=[Task],
                                      initializers=[task_init_func])
        return "Saved"
    return render_template('task/import.html')

@bp.route("/export", methods=['GET'])
def export():
    #return excel.make_response_from_tables(db.session, [Task], "xls")
    filtered_task = Task.query.filter_by(done=False).all()
    column_names = ['id', 'area', 'content']
    #eturn excel.make_response_from_tables(db.session, [Task], "xls")
    return excel.make_response_from_query_sets(filtered_task, column_names, "xls")
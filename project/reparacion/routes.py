from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
import flask_excel as excel


import json

from project.reparacion import bp
from project import db

from project.models import *
from .forms import ReparacionForm


@bp.route('/')
#@login_required
def list():
    reparaciones = Reparacion.query.all()
    return render_template('reparacion/list.html', reparaciones=reparaciones)


@bp.route('/reparacion', methods=['POST', 'GET'])
@login_required
def add_reparacion():
    title = "Add Reparacion"
    form = ReparacionForm()
    form.maquina_id.choices = [(x.id, x.name) for x in Maquina.query.all()]
    
    if form.validate_on_submit():
        content = request.form.get('content')
        reparacion = Reparacion(content)
        reparacion.maquina_id = form.maquina_id.data
        db.session.add(reparacion)
        db.session.commit()
        return redirect(url_for('reparacion.list'))
    return render_template('reparacion/reparacion.html', title=title, form=form)


@bp.route('/modify/<int:reparacion_id>', methods=['GET', 'POST'])
@login_required
def modify_reparacion(reparacion_id):
    title='Actualiza reparacion'
    reparacion = Reparacion.query.get(reparacion_id)
    form = ReparacionForm(obj=reparacion)
    form.maquina_id.choices = [(x.id, x.name) for x in Maquina.query.all()]

    if form.validate_on_submit():
        #reparacion = request.form[form]
        reparacion.content = form.content.data
        reparacion.maquina_id = form.maquina_id.data
        reparacion.created = form.created.data
        reparacion.modify = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('reparacion.list'))
    elif request.method == 'GET':
        form.populate_obj(reparacion)
        #form.content.data = task.content
        #form.maquina_id.data = task.maquina_id
    return render_template('reparacion/modify_reparacion.html', title=title, reparacion=reparacion,
        form=form)



@bp.route("/export", methods=['GET'])
def export():
    #filtered_task = Reparacion.query.filter_by(done=False).all()
    #column_names = ['id', 'content']
    #return excel.make_response_from_query_sets(filtered_task, column_names, "xls")
    return excel.make_response_from_tables(db.session, [Reparacion, Maquina], "xls")
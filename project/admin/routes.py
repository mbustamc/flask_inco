
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
import flask_excel as excel



from project.admin import bp
from project import db

from project.models import *

from .forms import *

@bp.route('/area')
#@login_required
def list_area():
    areas = Area.query.all()
    return render_template('admin/list_area.html', areas=areas)


@bp.route('/add_area', methods=['POST', 'GET'])
@login_required
def add_area():
    title = "Add Area"
    form = AreaForm()

    #areas = Area.query.all()
    #form.areas.choices = [(areas.id, areas.nombre) for areas in Area.query.all()]

    if form.validate_on_submit():
        area = Area()
        form.populate_obj(area)
        db.session.add(area)
        db.session.commit()
        return redirect(url_for('admin.list_area'))
    return render_template('admin/add_area.html', title=title, form=form)
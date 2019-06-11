from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from project.auth import bp
from project import db

from project.models import User

from .forms import LoginForm, RegistrationForm, EditProfileForm



@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@bp.route("/")
@login_required
def index():
    return redirect(url_for('main.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
	title='Sign In'
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page:
			next_page = url_for('main.index')
		return redirect(next_page)
	return render_template('auth/login.html', title=title, form=form)



@bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
	title='Register'
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title=title, form=form)


@bp.route('/user/<username>')
#@login_required
def user(username):
	title='Ver perfil'
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('auth/user.html', title=title, user=user)



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	title='Actualiza tu perfil'
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('auth.user', username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('auth/edit_profile.html', title=title,
		form=form)
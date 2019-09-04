#models/auth.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from hashlib import md5
# Local Imports
from project import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
            return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    maquinas = db.relationship('Maquina', backref='area', lazy='dynamic')
    tareas = db.relationship('Task', backref='area', lazy='dynamic')

    def __repr__(self):
        return '%s' % self.name


class Maquina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    
    reparaciones = db.relationship('Reparacion', backref='maquina', lazy='dynamic')

    def __repr__(self):
        return '%s' % self.name


class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    tareas = db.relationship('Task', backref='estado', lazy='dynamic')

    def __repr__(self):
        return '%s' % self.name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))

    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self, content):
        self.content = content
        #self.done = done

    def __repr__(self):
        return '%s' % self.content


class Reparacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maquina_id = db.Column(db.Integer, db.ForeignKey('maquina.id'))
    detencion_id = db.Column(db.Integer, db.ForeignKey('detencion.id'))
    duracion = db.Column(db.Integer)
    comentarios = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modify = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self):
        self.created = datetime.utcnow
        #self.done = done

    def __repr__(self):
        return '%s %s' % self.detencion_id, self.created


class Detencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    reparaciones = db.relationship('Reparacion', backref='detencion', lazy='dynamic')


    def __init__(self):
        pass
        #self.name = name
        #self.done = done

    def __repr__(self):
        return '%s' % self.name


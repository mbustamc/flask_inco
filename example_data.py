#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project import create_app
from project.models import *


app = create_app()
app.app_context().push()


def do_work():
    with app.app_context():
     
        administrador = User(username= 'mbustamc', email='mbustamc@gmail.com', is_admin=True)
        administrador.set_password('password')

        db.session.add(administrador)
        db.session.commit()	


do_work()
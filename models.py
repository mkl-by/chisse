from app import db
from flask_security import UserMixin, RoleMixin
import datetime

roles_users=db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                     )
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


turnirs_player=db.Table('turnirs_player',
                 db.Column('turnir_id', db.Integer, db.ForeignKey('turnir.id'), primary_key=True),
                 db.Column('chplayers_id', db.Integer, db.ForeignKey('chisse_player.id'), primary_key=True)
                 )

class ChissePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    patronymic = db.Column(db.String(255))
    name_by = db.Column(db.String(255))
    lastname_by = db.Column(db.String(255))
    name_en=db.Column(db.String(255))
    lastname_en=db.Column(db.String(255))
    datebirt = db.Column(db.DateTime)
    rating=db.Column(db.Integer)
    international_rating=db.Column(db.Integer)
    fido = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True, nullable=True)
    turnirs=db.relationship('Turnir', secondary=turnirs_player, lazy='subquery', backref=db.backref('chisseturnirs', lazy=True))

    def __repr__(self):
        if self.active:
            return '{0} {1}'.format(self.lastname, self.name)
        else:
            return 'Шахматист в клубе больше не занимается'

class Turnir(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name_turnir=db.Column(db.String(100))
    table_turnir=db.Column(db.PickleType)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow) #дата создания
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    #сhisseplayer_id=db.Column(db.Integer, db.ForeignKey('chisse_player.id'))

    # Пример один ко многим другой вариант!!!!!!!!!!!!!
    #
    # class DomainRoot(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #
    # class DomainPath(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     root_id = db.Column(db.ForeignKey(DomainRoot.id))
    #     root = db.relationship(DomainRoot, backref='paths')
    #
    # db.create_all()
    # db.session.add(DomainRoot(paths=[DomainPath(), DomainPath()]))
    # db.session.commit()
    # print(DomainRoot.query.get(1).paths)
from flask import Flask, url_for

from flask_security import SQLAlchemyUserDatastore, Security
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
#from flask_admin.contrib.fileadmin import FileAdmin
from flask_wtf.csrf import CSRFProtect

from flask_bootstrap import Bootstrap

from os import path as ospa

#приложение
app = Flask(__name__)
app.config.from_object(Configuration)

#bootstrap
Bootstrap(app)

#база
db=SQLAlchemy(app)

csrf = CSRFProtect(app)

#миграции
migrate=Migrate(app, db)
manager=Manager(app)
manager.add_command('db', MigrateCommand) #Создаем команду db для мигаций

#ADMIN
from admin import AdminView, HomeAdminView
from models import *

admin=Admin(app, 'Flask Admin', url='/', index_view=HomeAdminView(name='Home')) #url-перенаправляем на наш сайт если юзер не админ
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(ChissePlayer, db.session))
admin.add_view(AdminView(Turnir, db.session))
#при необходимости показываем файлы
# path = ospa . join ( ospa . dirname ( __file__ ), 'static' )
# admin . add_view ( FileAdmin ( path , '/static/' , name = 'Static Files' ))

#установка секюрити
user_datastore=SQLAlchemyUserDatastore(db, User, Role) #объект хранит юзеров и роли
security=Security(app, user_datastore)

#регистрируем блюпринты
from statis.statistic import statistic
from swiss.swiss_sistem import swiss_sistem
app.register_blueprint(statistic, url_prefix='/statistic')
app.register_blueprint(swiss_sistem, url_prefix='/swiss_sistem')

#изменения в jinja2 создаем фильтр даты
# def format_datetime(value, format='year'):
#     return value.
# app.jinja_env.filters['dat']=format_datetime

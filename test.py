# from app import db
# from models import ChissePlayer
# import time
# player=ChissePlayer.query.order_by(ChissePlayer.name).all()
# a=time.time()
# len(player)
# #quantity=db.session.query(ChissePlayer).count() #колличество играков
# b=time.time()
# print(b-a)

# from flask_wtf.form import FlaskForm, Form
#
# #from wtforms.widgets.html5 import
# from wtforms import SelectField
# from wtforms.widgets import Select, TableWidget
# from wtforms.fields import SelectMultipleField, FormField
# from wtforms import fields
#
#
# class UpdateWidgetForm(FlaskForm):
#     widget_number = fields.IntegerField()
#     widget_policy = fields.SelectField(choices=[('foo', 'Foo'), ('bar', 'Bar')])
#
# class UpdateMultipleWidgetsForm(FlaskForm):
#     widgets = fields.FieldList(FormField(UpdateWidgetForm))
#
# f=UpdateMultipleWidgetsForm()
# print(f)


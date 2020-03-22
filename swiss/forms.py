from flask_wtf.form import FlaskForm, Form

#from wtforms.widgets.html5 import
from wtforms import SelectField
from wtforms.widgets import Select, TableWidget
from wtforms.fields import SelectMultipleField, FormField
from wtforms import fields
from wtforms.validators import DataRequired, NumberRange

class SelectForm(FlaskForm):
    widget_policy = fields.SelectField(label='Выберте диапазон дат рождения игроков')
    end_data = fields.SelectField()
    submint = fields.SubmitField('выбор')
# class UpdateMultipleWidgetsForm(FlaskForm):
#     widgets = fields.FieldList(FormField(UpdateWidgetForm))
#
class Nameturnir(FlaskForm):
    nameturnir=fields.StringField('nameturnir', default='введите наименование турнира', validators=[DataRequired()])
    #написать валидацию для если пользователь ввел название как дефолтное значение
    # submint = fields.SubmitField('выбор')
class Point(FlaskForm):

    point=fields.FloatField('point', validators=[(NumberRange(0,2,'введено недопустимое колличество очков')) ])
    
class Points(FlaskForm):
    points=fields.FieldList(fields.FormField(Point), min_entries=1)

class TableForm(FlaskForm):

    #language = SelectField(u'Programming Language', choices=[(1,'s'),(2,'e'),(3,'t')])
    #players=SelectMultipleField()
    chek=fields.SelectMultipleField()

    # text=fields.HiddenField() option_widget=['RadioField','StringField']
    submint=fields.SubmitField('выбор')

# class SelectMultipleFormField(SelectMultipleField):
#
#     widget = SelectMultipleField
#
#     def __init__(
#             self, max_length=None, size=4, max_choices=None,
#             max_choices_attr=DEFAULT_MAX_CHOICES_ATTR,
#             *args, **kwargs):
#         """
#         max_length refers to number of characters used to store the encoded
#         list of choices (est. 2n - 1)
#         size is the HTML element size attribute passed to the widget
#         max_choices is the maximum number of choices allowed by the field
#         max_choices_attr is a string used as an attribute name in the widget
#         representation of max_choices (currently a data attribute)
#         coerce is bound to ModelField.to_python method when using
#         ModelViewMixin, otherwise it returns what is passed (the identity
#         function)
#         empty_value is the value used to represent an empty field
#         """
#         self.max_length, self.max_choices = max_length, max_choices
#         self.size, self.max_choices_attr = size, max_choices_attr
#         self.coerce = kwargs.pop('coerce', lambda val: val)
#         self.empty_value = kwargs.pop('empty_value', [])
#         if not hasattr(self, 'empty_values'):
#             self.empty_values = list(validators.EMPTY_VALUES)
#         super(SelectMultipleFormField, self).__init__(*args, **kwargs)
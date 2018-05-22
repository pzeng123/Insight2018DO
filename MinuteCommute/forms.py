from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import Required, Email


class Addressform(FlaskForm):
    address = TextField(u'Address', validators=[Required()])
    submit = SubmitField(u'Submit')

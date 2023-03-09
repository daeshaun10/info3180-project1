from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired


class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    desc = TextAreaField("Description", validators=[InputRequired()])
    rooms = IntegerField("Rooms", validators=[InputRequired()])
    bathrooms = IntegerField("Bathrooms", validators=[InputRequired()])
    price = IntegerField("Price", validators=[InputRequired()])
    propertytype = SelectField("Propertytype", choices=["House", "Apartment"])
    location = StringField('location', validators=[InputRequired()])
    upload = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


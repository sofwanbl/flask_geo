from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    zosm_id=StringField("Id OSM")
    zname=StringField("Name")
    zoperatorty=StringField("Type")
    zaddrcity=StringField("City")
    zaddrfull=StringField("Address")
    zamenity = StringField("Type of Building")
    zsource = StringField("Data Source")
    zgeom = StringField("Geometry")
    submit=SubmitField("Edit")
    submit_entry=SubmitField("Save")

class CariForm(FlaskForm):
    wname = StringField("Name of Building")
    submit_cari = SubmitField("Search")
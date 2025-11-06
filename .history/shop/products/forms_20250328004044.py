from flask_wtf.file import FileAllowed, FileField

from wtforms import Form,StringField, IntegerField, BooleanField, TextAreaField, validators, DecimalField,SubmitField,SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm  # Cette ligne doit être en haut du fichier




class AddProducts(Form):
    name = StringField("Name", [validators.DataRequired()])
    price = IntegerField("Price:RS ", [validators.DataRequired()])
    stock = IntegerField("Stock", [validators.DataRequired()])
    desc = TextAreaField("Description", [validators.DataRequired()])
    # colors = TextAreaField("Colors", [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'])])



class OrderConfirmationForm(FlaskForm):
    gender = SelectField('Genre', choices=[('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()])
    age = IntegerField('Âge', validators=[DataRequired(), NumberRange(min=18, max=99)])
    product_category = SelectField('Catégorie', choices=[
        ('electronics', 'Électronique'),
        ('clothing', 'Vêtements'),
        ('food', 'Alimentation')
    ], validators=[DataRequired()])
    price_per_unit = FloatField('Prix moyen', validators=[DataRequired()])
    delivery_address = TextAreaField('Adresse', validators=[DataRequired()])
    payment_method = SelectField('Paiement', choices=[
        ('credit', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('cash', 'Espèces')
    ], validators=[DataRequired()])
    photo = FileField('Photo de confirmation', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement (JPG, PNG)')
    ])
    submit = SubmitField('Confirmer')
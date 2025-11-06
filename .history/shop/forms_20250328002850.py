# Dans forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed

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
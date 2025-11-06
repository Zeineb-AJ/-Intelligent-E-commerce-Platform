from flask_wtf.file import FileAllowed, FileField

from wtforms import Form,StringField, IntegerField, BooleanField, TextAreaField, validators, DecimalField,SubmitField,SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange,InputRequired
from flask_wtf import FlaskForm  # Cette ligne doit être en haut du fichier

from flask_wtf.file import FileAllowed, FileRequired
from decimal import Decimal



class AddProducts(FlaskForm):  # Hérite de FlaskForm au lieu de Form
    name = StringField('Nom du Produit', validators=[
        DataRequired(message="⚠ Champ obligatoire"),
    ])
    
    price = DecimalField('Prix (RS)', validators=[
        DataRequired(message="⚠ Champ obligatoire"),
        NumberRange(min=0.01, message="⚠ Prix invalide")
    ], places=2)
    
    stock = IntegerField('Stock', validators=[
        DataRequired(message="⚠ Champ obligatoire"),
        NumberRange(min=0, message="⚠ Stock invalide")
    ])
    
    desc = TextAreaField('Description', validators=[
        DataRequired(message="⚠ Champ obligatoire"),
    ])
    
    image_1 = FileField('Image Principale', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], message="⚠ Formats: JPG, PNG, WEBP")
    ])


class OrderConfirmationForm(FlaskForm):
    gender = SelectField('Genre', choices=[('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()])
    age = IntegerField('Âge', validators=[DataRequired(), NumberRange(min=18, max=99)])
    product_category = SelectField('Catégorie', choices=[
        ('electronics', 'Électronique'),
        ('clothing', 'Vêtements'),
        ('food', 'Alimentation')
    ], validators=[DataRequired()])
    price_per_unit = FloatField('Prix moyen', validators=[InputRequired()])
    delivery_address = TextAreaField('Adresse', validators=[DataRequired()])
    payment_method = SelectField('Paiement', choices=[
        ('credit', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('cash', 'Espèces')
    ], validators=[DataRequired()])
    submit = SubmitField('Confirmer')
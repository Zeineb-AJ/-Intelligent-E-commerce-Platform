from flask_wtf.file import FileAllowed, FileField

from wtforms import Form,StringField, IntegerField, BooleanField, TextAreaField, validators, DecimalField,SubmitField,SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange,InputRequired
from flask_wtf import FlaskForm  # Cette ligne doit être en haut du fichier

from flask_wtf.file import FileAllowed, FileRequired
from decimal import Decimal

class AddProducts(Form):
    name = StringField("Nom du produit", [
        validators.DataRequired(message="Le nom du produit est obligatoire"),
        validators.Length(min=3, max=100, message="Le nom doit contenir entre 3 et 100 caractères")
    ])
    
    price = IntegerField("Prix (RS)", [
        validators.DataRequired(message="Le prix est obligatoire"),
        validators.NumberRange(min=1, message="Le prix doit être supérieur à 0")
    ])
    
    stock = IntegerField("Stock", [
        validators.DataRequired(message="La quantité en stock est obligatoire"),
        validators.NumberRange(min=0, message="Le stock ne peut pas être négatif")
    ])
    
    desc = TextAreaField("Description", [
        validators.DataRequired(message="La description est obligatoire"),
        validators.Length(min=10, message="La description doit contenir au moins 10 caractères")
    ])
    
    image_1 = FileField('Image principale', [
        FileRequired(message="Une image est requise"),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], message="Formats acceptés: JPG, JPEG, PNG, WEBP")
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
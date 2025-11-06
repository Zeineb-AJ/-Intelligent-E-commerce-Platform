from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import Form,StringField, IntegerField, BooleanField, TextAreaField, validators, DecimalField,SubmitField,SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange,InputRequired,Optional
from flask_wtf import FlaskForm  # Cette ligne doit être en haut du fichier


class AddProducts(FlaskForm):
    name = StringField("Name", [DataRequired()])
    price = DecimalField("Price (RS)", [DataRequired()], places=2)
    stock = IntegerField("Stock", [DataRequired()])
    desc = TextAreaField("Description", [DataRequired()])

    # Ajout du champ discount (remise)
    discount = DecimalField("Discount (%)", [Optional()], places=2, default=0.0)

    # Ajout du champ sales (nombre de ventes)
    sales = IntegerField("Number of Sales", [Optional()], default=0)

    # Ajout du champ active (actif ou non)
    active = SelectField("Active", choices=[(1, "Yes"), (0, "No")], coerce=int, default=1)

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'])])



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
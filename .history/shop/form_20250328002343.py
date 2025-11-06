from flask_wtf.file import FileField, FileAllowed

class OrderConfirmationForm(FlaskForm):
    gender = SelectField('Genre', choices=[('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()])
    age = IntegerField('Âge', validators=[DataRequired(), NumberRange(min=18, max=99)])
    product_category = SelectField('Catégorie', choices=[
        ('electronics', 'Électronique'),
        ('clothing', 'Vêtements'),
        ('food', 'Alimentation')
    ])
    price_per_unit = FloatField('Prix moyen', validators=[DataRequired()])
    delivery_address = TextAreaField('Adresse', validators=[DataRequired()])
    payment_method = SelectField('Paiement', choices=[
        ('credit', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('cash', 'Espèces')
    ])
    photo = FileField('Photo de confirmation', validators=[
        FileAllowed(['jpg', 'png'], 'Images seulement!')
    ])
    submit = SubmitField('Confirmer')
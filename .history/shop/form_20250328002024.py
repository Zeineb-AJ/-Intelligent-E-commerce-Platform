from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired

class AnalyticsDataForm(FlaskForm):
    customer_id = IntegerField('ID Client', validators=[DataRequired()])
    gender = SelectField('Genre', choices=[('M', 'Masculin'), ('F', 'Féminin')])
    age = IntegerField('Âge', validators=[DataRequired()])
    product_category = StringField('Catégorie Produit', validators=[DataRequired()])
    quantity = IntegerField('Quantité', validators=[DataRequired()])
    price_per_unit = FloatField('Prix Unitaire', validators=[DataRequired()])
    # total_amount sera calculé automatiquement
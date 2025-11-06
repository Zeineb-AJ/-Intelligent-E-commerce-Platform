from shop import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)  # Nouveau champ pour les promotions (en pourcentage)
    stock = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    sales = db.Column(db.Integer, default=0)  # Nouveau champ pour suivre les ventes
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))
    image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name
    
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('register_model.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="En attente")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation corrigée - utilisez le nom de la classe Python
    user = db.relationship('RegisterModel', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
    

class Confirm_Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    customer_id = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    product_category = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    delivery_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order = db.relationship('Order', backref='analytics')
   
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Relation entre OrderItem et Order
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    
    # Relation entre OrderItem et Product
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))


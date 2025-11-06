import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Product, Brand, Category,Order,OrderItem


@app.route("/admin")
def admin():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    products = Product.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)

@app.route('/brands')
def brands():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brands Page", brands=brands)

@app.route('/categories')
def categories():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories.html', title="Categories Page", categories=categories)

@app.route('/order', methods=['POST'])
def orders():
    if "email" not in session:
        flash("Veuillez vous connecter", "danger")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=session['email']).first()
    cart = session.get("cart", {})  # Le panier est stocké en session

    if not cart:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for("shop"))

    # Création de la commande
    order = Order(user_id=user.id, total_price=0, status="En attente")
    db.session.add(order)
    db.session.commit()  # Commit ici pour générer un ID d'ordre

    total_price = 0

    # Ajouter les produits de la commande
    for product_id, item in cart.items():
        product = Product.query.get(product_id)
        if product:
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item['quantity'])
            db.session.add(order_item)
            total_price += item['quantity'] * product.price

    # Mettre à jour le prix total et valider
    order.total_price = total_price
    db.session.commit()

    # Vider le panier après l'achat
    session["cart"] = {}

    flash("Commande passée avec succès !", "success")
    return redirect(url_for("orders"))




@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        #hash_password = bcrypt.generate_password_hash(form.password.data)
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.name.data},Thank You for registering", "success")
        return redirect(url_for("login"))
    return render_template("admin/register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(f"Welcome, {user.username}. You are now logged in.", "success")
            return redirect(url_for("admin"))

    return render_template("admin/login.html", form=form, title="Log In")


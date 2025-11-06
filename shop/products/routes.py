from flask import  Blueprint,redirect, url_for, request, flash, render_template, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Product,Order,Confirm_Order,OrderItem
from .forms import AddProducts
import secrets, os
from .forms import OrderConfirmationForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import joblib

from flask import render_template
from datetime import datetime
import pandas as pd

from sqlalchemy import func


from datetime import datetime

import logging



@app.route('/confirm_order', methods=['GET', 'POST'])
@login_required
def confirm_order():
    if not session.get('shopcart') or len(session['shopcart']) == 0:
        flash('Votre panier est vide !', 'warning')
        return redirect(url_for('products.cart'))

    form = OrderConfirmationForm(request.form if request.method == 'POST' else None)

    # Debug: Afficher les données reçues
    if request.method == 'POST':
        print("Données POST reçues:", request.form)
        print("Erreurs de validation:", form.errors)

    if form.validate_on_submit():
        try:
            # Calcul des totaux
            cart_items = session['shopcart'].values()
            total_price = sum(float(p['price']) * int(p['quantity']) for p in cart_items)
            total_quantity = sum(int(p['quantity']) for p in cart_items)

            # Création de la commande
            new_order = Order(
                user_id=current_user.id,
                total_price=total_price,
                status="En attente",
                created_at=datetime.utcnow()
            )
            db.session.add(new_order)
            db.session.flush()  # Génère l'ID sans commit

            # Création de la confirmation
            confirm_data = Confirm_Order(
                order_id=new_order.id,
                customer_id=current_user.id,
                gender=form.gender.data,
                age=form.age.data,
                product_category=form.product_category.data,
                quantity=total_quantity,
                price_per_unit=round(total_price/total_quantity, 2) if total_quantity > 0 else 0,
                total_amount=total_price,
                delivery_address=form.delivery_address.data,
                payment_method=form.payment_method.data
            )
            db.session.add(confirm_data)
            db.session.commit()

            session.pop('shopcart')
            flash('Commande confirmée avec succès!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur commande: {str(e)}", exc_info=True)
            flash(f"Erreur technique: {str(e)}", 'danger')
            return redirect(url_for('products.cart'))

    # Pré-remplissage pour GET
    if request.method == 'GET':
        form.gender.data = 'M'  # Valeur par défaut
        if session['shopcart']:
            prices = [float(p['price']) for p in session['shopcart'].values()]
            form.price_per_unit.data = round(sum(prices)/len(prices), 2) if prices else 0

    return render_template('products/confirm.html',
                         form=form,
                         cart=session['shopcart'],
                         total=sum(float(p['price'])*int(p['quantity']) 
                               for p in session['shopcart'].values()))
 
def get_all_brands():
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    return brands

def get_all_categories():
    return Category.query.join(Product, (Category.id==Product.category_id)).all()

@app.route('/')
def home():
    # Vos requêtes existantes
    promo_products = Product.query.filter(Product.discount > 0).limit(3).all()
    new_products = Product.query.order_by(Product.pub_date.desc()).limit(3).all()
    trend_products = Product.query.order_by(Product.sales.desc()).limit(3).all()
    
 
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(active=True).paginate(page=page, per_page=8)
    
    return render_template('products/index.html',
                         products=products,
                         promo_products=promo_products,
                         trend_products=trend_products,
                         new_products=new_products,
                         
                         brands=get_all_brands(), 
                         categories=get_all_categories())


@app.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id==Product.category_id)).all()
    return render_template('products/product_details.html', product=product, title=product.name, brands=brands, 
                    categories=get_all_categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand = get_b).paginate(page=page, per_page=4)
    return render_template('products/index.html', brand=brand, title=Brand.query.get(id).name, brands=get_all_brands(), 
    categories=get_all_categories(), get_b=get_b)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Product.query.filter_by(category = get_cat).paginate(page=page, per_page=4)
    return render_template('products/index.html', category=category, title=Category.query.get(id).name, 
                            categories=get_all_categories(), brands=get_all_brands(), get_cat=get_cat)


@app.route('/addbrand', methods=["GET", "POST"])
def addbrand():
    if request.method == "POST":
        getBrand = request.form.get('brand')
        brand = Brand(name=getBrand)
        db.session.add(brand)
        flash(f'The Brand {getBrand} was added to DataBase.', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Add Brand', brands='brands')

@app.route('/addcategory', methods=["GET", "POST"])
def addcategory():
    if request.method == "POST":
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        flash(f'The Category {getCategory} was added to DataBase.', 'success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html', title='Add Category')

@app.route('/addproduct', methods=["GET", "POST"])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        desc = form.desc.data
        brand_id = request.form.get('brand')
        category_id = request.form.get('category')
        print(f"Brand ID:{brand_id}, Category Id:{category_id}")
        # category = Category.query.get(id=category_id).first()
        # brand = Brand.query.get(id=brand_id).first()
        # print(f"Brand:{brand}, Category:{category}")
        image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        print(f"Image 1 name:{image_1}, its type:{type(image_1)}")
        product = Product(name=name, price=price, stock=stock, desc=desc, brand_id=brand_id, 
        category_id=category_id, image_1=image_1)
        db.session.add(product)
        flash(f"{name} has been added to database.", 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Product', form=form, brands=brands, 
                            categories=categories)

@app.route('/updatebrand/<int:id>', methods=["GET", "POST"])
def updatebrand(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title="Update Brand Info", 
                            updatebrand=updatebrand)

@app.route('/updatecategory/<int:id>', methods=["GET", "POST"])
def updatecategory(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title="Update category Info", 
                            updatecategory=updatecategory)    
@app.route('/updateproduct/<int:id>', methods=["GET", "POST"])
def updateproduct(id):
    current_app.logger.info(f"Mise à jour du produit ID: {id}")
    
    # Vérification de l'authentification
    if 'email' not in session:
        flash('Veuillez vous connecter d\'abord', 'danger')
        return redirect(url_for('login'))

    # Initialisation des données
    product = Product.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form, obj=product)  # Pré-remplir avec les valeurs actuelles

    if request.method == "POST":
        try:
            current_app.logger.info(f"Données soumises: {request.form}")
            
            # Validation des données
            if not form.validate():
                flash('Veuillez corriger les erreurs dans le formulaire', 'danger')
                current_app.logger.warning(f"Erreurs de validation: {form.errors}")
                return render_template('products/updateproduct.html', 
                                       form=form, 
                                       brands=brands,
                                       categories=categories, 
                                       product=product)

            # Conversion et validation du prix
            try:
                price = int(form.price.data)
                if price <= 0:
                    raise ValueError("Le prix doit être positif")
            except (ValueError, TypeError) as e:
                flash('Prix invalide - doit être un nombre entier positif', 'danger')
                current_app.logger.error(f"Erreur conversion prix: {e}")
                return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

            # Mise à jour des champs
            product.name = form.name.data
            product.price = price
            product.stock = int(form.stock.data)
            product.desc = form.desc.data
            product.brand_id = int(request.form.get('brand'))
            product.category_id = int(request.form.get('category'))
            product.discount = request.form.get('discount', 0)
            
            current_app.logger.info(f"Mise à jour du produit: {product.name}, Prix: {product.price}, Stock: {product.stock}")

            # Gestion de l'image
            if 'image_1' in request.files and request.files['image_1'].filename != '':
                image = request.files['image_1']
                if allowed_file(image.filename):
                    if product.image_1:
                        try:
                            os.remove(os.path.join(current_app.root_path, 'static/images', product.image_1))
                        except OSError as e:
                            current_app.logger.error(f"Erreur suppression image: {str(e)}")
                    
                    filename = secrets.token_hex(10) + os.path.splitext(image.filename)[1]
                    image.save(os.path.join(current_app.root_path, 'static/images', filename))
                    product.image_1 = filename
                    current_app.logger.info(f"Image mise à jour: {filename}")

            # Commit des modifications
            db.session.commit()
            flash('Produit mis à jour avec succès', 'success')
            current_app.logger.info("Mise à jour réussie")
            return redirect(url_for('admin'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur mise à jour produit: {str(e)}")
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')
            return redirect(url_for('updateproduct', id=id))

    return render_template('products/updateproduct.html', 
                           title="Modifier Produit", 
                           form=form, 
                           brands=brands,
                           categories=categories, 
                           product=product)
@app.route('/deletebrand/<int:id>', methods=["POST"])
def deletebrand(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'Brand: {brand.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Brand: {brand.name} cant be Deleted', 'warning')
    return redirect(url_for('admin'))

@app.route('/deletecategory/<int:id>', methods=["POST"])
def deletecategory(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Category: {category.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Category: {category.name} cant be Deleted', 'warning')
    return redirect(url_for('admin'))

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    if 'email' not in session:
        flash('Please Log In first', 'danger')
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} Deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Cant delete {product.name}', 'warning')
    return redirect(url_for('admin'))


@app.route("/orders/update/<int:order_id>", methods=["POST"])
def update_order(order_id):
    if "email" not in session:
        flash("Veuillez vous connecter", "danger")
        return redirect(url_for("login"))

    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    if new_status:
        order.status = new_status
        db.session.commit()
        flash(f"Statut de la commande {order.id} mis à jour !", "success")
    
    return redirect(url_for("orders"))

@app.route("/orders/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    if "email" not in session:
        flash("Veuillez vous connecter", "danger")
        return redirect(url_for("login"))

    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f"Commande {order.id} supprimée !", "success")
    
    return redirect(url_for("orders"))
@app.route('/order/<int:order_id>', methods=['GET'])
def order_details(order_id):
    order = Order.query.get(order_id)  # Récupérer la commande par ID
    if not order:
        abort(404)  # Retourner une erreur si la commande n'existe pas
    
    order_items = OrderItem.query.filter_by(order_id=order.id).all()  # Récupérer les produits achetés

    return render_template('admin/order_details.html', order=order, order_items=order_items)


@app.route('/dashboard')
def admin_dashboard():
    # --- 1. Charger le modèle ---
    chemin_modele = r'C:\Users\Zeineb\Desktop\TEKUP\ProjetBI\models\vente_prediction_model.pkl'
    model = joblib.load(chemin_modele)

    # --- 2. Préparer les données futures pour 12 mois ---
    future_dates = pd.date_range(start=datetime.today(), periods=12, freq='MS')
    future_df = pd.DataFrame({'YearMonth': future_dates})
    future_df['Month'] = future_df['YearMonth'].dt.month
    future_df['Year'] = future_df['YearMonth'].dt.year

    # --- 3. Valeurs par défaut ---
    future_df['Sales'] = 100
    future_df['RollingMean'] = future_df['Sales'].rolling(window=3).mean().shift(1)
    future_df['MonthGrowth'] = future_df['Sales'].pct_change().shift(1)

    # --- 4. Colonnes catégories attendues ---
    for col in model.feature_names_in_:
        if col.startswith('product_category_'):
            future_df[col] = 1

    future_X = future_df[model.feature_names_in_]
    y_pred = model.predict(future_X)

    pred_labels = [date.strftime('%Y-%m') for date in future_df['YearMonth']]
    pred_values = y_pred.tolist()

    # --- 5. Top 5 catégories les plus vendues ---
    top_categories = db.session.query(
        Confirm_Order.product_category,
        func.sum(Confirm_Order.quantity).label('total_sales')
    ).group_by(Confirm_Order.product_category)\
     .order_by(func.sum(Confirm_Order.quantity).desc())\
     .limit(5).all()

    labels = [cat for cat, _ in top_categories]
    sales = [qty for _, qty in top_categories]

    # --- 6. KPI ---
    total_sales = db.session.query(db.func.sum(Confirm_Order.total_amount)).scalar()
    total_orders = Confirm_Order.query.count()
    total_products = Product.query.count()
    total_categories = Category.query.count()

    # --- 7. Graphe : Nombre de produits par catégorie ---
    
    # Produits par catégorie pour le graphique
    category_data = db.session.query(
        Category.name,
        func.count(Product.id).label('product_count')
    ).join(Product, Product.category_id == Category.id)\
     .group_by(Category.name).all()

    category_names = [cat[0] for cat in category_data]
    category_counts = [cat[1] for cat in category_data]

    # --- 8. Récupérer les commandes par statut ---
 # Récupérer les statuts de commande et le nombre de commandes pour chaque statut
    status_data = db.session.query(
        Order.status,
        func.count(Order.id).label('order_count')
    ).group_by(Order.status).all()

    # Préparer les labels et les valeurs pour le graphique
    order_status_labels = [f'{status} ({count})' for status, count in status_data]
    order_status_counts = [count for _, count in status_data]

    

    # --- 8. Rendu ---
    return render_template('admin/dashboard.html',
                           labels=labels,
                           sales=sales,
                           prediction_labels=pred_labels,
                           prediction_values=pred_values,
                           total_sales=total_sales,
                           total_orders=total_orders,
                           total_products=total_products,
                           total_categories=total_categories,
                           top_selling_categories=top_categories,
                           category_names=category_names,
                           category_counts=category_counts,
                           order_status_labels=order_status_labels,
                           order_status_counts=order_status_counts)
                           

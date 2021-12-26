from application import app, models, db
from flask import render_template, request, json, Response, jsonify, redirect, flash, url_for
from application.models import User, Enrollment, Supplier, IncomingProduct, ProductSupplier
from application.forms import RegistrationForm, SupplierForm, IncomingProductForm

import os


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form.get('term')
    user_id = 1
    if id:
        if Enrollment.query.filter_by(course_id=id, user_id=user_id).first():
            flash(f"Oops! Already registered in this course {title}", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, course_id=id)
            flash(f"Successfully Enrolled in {title}", "success")
    classes = None
    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)


@app.route("/getall")
def get_all():
    try:
        users = User.query.all()
        # return jsonify([e.serialize() for e in users])
        return render_template('user.html', users=users)
    except Exception as e:
        return(str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        user = User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return(str(e))


@app.route("/qr_code/<sku_id>", methods=['GET'])
def get_qr_code(sku_id):
    # Import QRCode from pyqrcode
    import pyqrcode
    import png
    from pyqrcode import QRCode

    # Generate QR code
    url = pyqrcode.create(sku_id)

    # Create and save the svg file naming "myqr.svg"
    # url.svg("myqr.svg", scale=8)

    # Create and save the png file naming "myqr.png"
    url.png(os.path.join(
        app.config['QR_CODE_FOLDER'], sku_id + '.png'), scale=6)
    # buffer = io.BytesIO()
    # url.png(buffer)

    # print(list(buffer.getvalue()))

    return redirect(url_for('static', filename='images/'+sku_id + '.png'), code=301)


@app.route("/products/incoming")
def incoming_products(term=None):
    incoming_products_data = IncomingProduct.query.all()

    return render_template("incoming_products.html", incomingProductsData=incoming_products_data, incoming_product=True)


@app.route("/products/incoming/add", methods=["GET", "POST"])
def add_incoming_products():
    form = IncomingProductForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        location = form.location.data
        reorder_point = form.reorder_point.data
        demand = form.demand.data
        quantity = form.quantity.data
        supplier_id = form.supplier_id.data
        incoming_product = IncomingProduct(
            sku_id=sku_id,
            location=location,
            reorder_point=reorder_point,
            demand=demand,
            quantity=quantity
        )
        db.session.add(incoming_product)
        db.session.commit()
        product_supplier = ProductSupplier(
            product_id=incoming_product.id,
            product_sku_id=incoming_product.sku_id,
            supplier_id=supplier_id,
        )
        db.session.add(product_supplier)
        db.session.commit()
        flash("You have successfully added the Product", "success")
        return redirect(url_for('incoming_products'))
    return render_template("add_incoming_product.html", title="Add Incoming Product", form=form, add_incoming_product=True)


@app.route("/products/incoming/update", methods=["GET", "POST"])
def update_incoming_product():
    sku_id = request.form.get('sku_id')
    str_quantity = request.form.get('quantity')
    if not str_quantity:
        quantity = 0
    else:
        quantity = int(request.form.get('quantity'))
    if sku_id:
        if IncomingProduct.query.filter_by(sku_id=sku_id).first():
            incoming_product = IncomingProduct.query.filter_by(
                sku_id=sku_id).first()
            old_quantity = incoming_product.quantity
            new_quantity = old_quantity + quantity
            incoming_product.quantity = new_quantity
            db.session.commit()
            flash(f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("incoming_product_update.html", incoming_product_update=True, title="Update Incoming Product", incoming_product=incoming_product)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("incoming_products"))
    else:
        flash(f"Please provide skuId", "danger")
        return redirect(url_for("incoming_products"))


@app.route("/products/incoming/delete", methods=["POST"])
def delete_incoming_product():
    sku_id = request.form.get('sku_id')
    incoming_product = IncomingProduct.query.filter_by(sku_id=sku_id).first()
    if incoming_product is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("incoming_products"))
    db.session.delete(incoming_product)
    db.session.commit()
    flash(f"Deleted Product for {sku_id}", "success")
    return redirect(url_for("incoming_products"))


@app.route("/supplier/register", methods=["GET", "POST"])
def register_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        id = form.id.data
        location = form.location.data
        name = form.name.data
        lead_time = form.lead_time.data
        supplier = Supplier(
            id=id,
            location=location,
            name=name,
            lead_time=lead_time,
        )
        db.session.add(supplier)
        db.session.commit()
        flash("You have successfully registered the supplier", "success")
        return redirect(url_for('supplier'))
    return render_template("register_supplier.html", title="Register Supplier", form=form, register_supplier=True)


@app.route("/supplier", methods=["GET"])
def supplier(term=None):
    supplier_data = Supplier.query.all()

    return render_template("supplier.html", supplierData=supplier_data, supplier=True)

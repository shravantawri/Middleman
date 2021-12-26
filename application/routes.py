from application import app, models, db
from flask import render_template, request, json, Response, jsonify, redirect, flash, url_for
from application.models import User, RawItem, Enrollment, Supplier
from application.forms import LoginForm, RegistrationForm, ItemForm, SupplierForm

import os


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, You are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, Something went wrong", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/items/raw")
def raw_items(term=None):
    raw_item_data = RawItem.query.all()

    return render_template("raw_items.html", rawItemData=raw_item_data, raw_items=True)


@app.route("/items/raw/add", methods=["GET", "POST"])
def add_raw_items():
    form = ItemForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        category = form.category.data
        colour = form.colour.data
        size = form.size.data
        quantity = form.quantity.data
        raw_item = RawItem(
            sku_id=sku_id,
            category=category,
            colour=colour,
            size=size,
            quantity=quantity
        )
        db.session.add(raw_item)
        db.session.commit()
        flash("You have successfully added the Item", "success")
        return redirect(url_for('raw_items'))
    return render_template("register_item.html", title="Register Items", form=form, add_raw_items=True)


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


@app.route("/items/raw/quantity/add", methods=["GET", "POST"])
def add_item():
    sku_id = request.form.get('sku_id')
    quantity = request.form.get('quantity')
    if sku_id:
        if RawItem.query.filter_by(sku_id=sku_id).first():
            item = RawItem.query.filter_by(sku_id=sku_id).first()
            item.quantity = item.quantity + 1
            db.session.commit()
            flash(f"added item for {sku_id}, quantity: {quantity}", "success")
            return render_template("item_add.html", add_item=True, title="Add Item", item=item)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("raw_items"))
    else:
        flash(f"Please provide skuId", "danger")
        return redirect(url_for("raw_items"))


@app.route("/items/raw/quantity/delete", methods=["POST"])
def delete_item():
    sku_id = request.form.get('sku_id')
    item = RawItem.query.filter_by(sku_id=sku_id).first()
    if item is None:
        flash(f"Oops! No Item present for {sku_id}", "danger")
        return redirect(url_for("raw_items"))
    db.session.delete(item)
    db.session.commit()
    flash(f"Deleted Item for {sku_id}", "success")
    return redirect(url_for("raw_items"))


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


@app.route("/user")
def add_user():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return "User added. user id={}".format(user.id)
    except Exception as e:
        return(str(e))


@app.route("/add_raw_item")
def add_course():
    sku_id = request.args.get('sku_id')
    category = request.args.get('category')
    colour = request.args.get('colour')
    size = request.args.get('size')
    quantity = request.args.get('quantity')
    try:
        raw_item = RawItem(
            sku_id=sku_id,
            category=category,
            colour=colour,
            size=size,
            quantity=quantity
        )
        db.session.add(raw_item)
        db.session.commit()
        return "Raw Item added. raw item id={}".format(raw_item.id)
    except Exception as e:
        return(str(e))


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

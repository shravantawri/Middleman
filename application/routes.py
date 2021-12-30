import datetime
import os
from application import app, models, db
from flask import render_template, request, json, Response, jsonify, redirect, flash, url_for
from application.models import User, Enrollment, Supplier, IncomingProduct, ProductSupplier, PlainClothing, Embroidery, Htp
from application.forms import RegistrationForm, SupplierForm, AddPlainClothingForm, UpdatePlainClothingForm, AddPlainClothingForm, AddEmbroideryForm, AddHtpForm, UpdateEmbroideryForm, UpdateHtpForm


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


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
    incoming_products_data = IncomingProduct.query.order_by(
        IncomingProduct.updated_at.desc()).all()

    return render_template("incoming_products.html", incomingProductsData=incoming_products_data, incoming_product=True)


@app.route("/products/raw")
def raw_products(term=None):
    raw_product_data = IncomingProduct.query.order_by(
        IncomingProduct.updated_at.desc()).all()

    return render_template("raw_products.html", incomingProductsData=raw_product_data, raw_product=True)


@app.route("/products/raw/plain_clothing")
def view_plain_clothing(term=None):
    plain_clothing_data = PlainClothing.query.order_by(
        PlainClothing.updated_at.desc()).all()

    return render_template("plain_clothing.html", plainClothingData=plain_clothing_data, plain_clothing=True)


@app.route("/products/raw/embroidery")
def view_embroidery(term=None):
    embroidery_data = Embroidery.query.order_by(
        Embroidery.updated_at.desc()).all()

    return render_template("embroidery.html", embroideryData=embroidery_data, embroidery=True)


@app.route("/products/raw/htp")
def view_htp(term=None):
    htp_data = Htp.query.order_by(
        Htp.updated_at.desc()).all()

    return render_template("htp.html", htpData=htp_data, htp=True)


@app.route("/products/raw/plain_clothing/add", methods=["GET", "POST"])
def add_plain_clothing():
    form = AddPlainClothingForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        location = form.location.data
        reorder_point = form.reorder_point.data
        demand = form.demand.data
        total_quantity = form.total_quantity.data
        color = form.color.data
        material = form.material.data
        sleeve_type = form.sleeve_type.data
        size = form.size.data
        supplier_id = form.supplier_id.data
        plain_clothing = PlainClothing(
            sku_id=sku_id,
            location=location,
            reorder_point=reorder_point,
            demand=demand,
            total_quantity=total_quantity,
            color=color,
            sleeve_type=sleeve_type,
            material=material,
            size=size

        )
        db.session.add(plain_clothing)
        db.session.commit()
        product_supplier = ProductSupplier(
            product_id=plain_clothing.id,
            product_sku_id=plain_clothing.sku_id,
            supplier_id=supplier_id,
        )
        db.session.add(product_supplier)
        db.session.commit()
        flash("You have successfully added the Product", "success")
        return redirect(url_for('view_plain_clothing'))
    return render_template("add_plain_clothing.html", title="Add Plain Clothing", form=form, add_plain_clothing=True)


@app.route("/products/raw/embroidery/add", methods=["GET", "POST"])
def add_embroidery():
    form = AddEmbroideryForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        location = form.location.data
        reorder_point = form.reorder_point.data
        demand = form.demand.data
        total_quantity = form.total_quantity.data
        color = form.color.data
        supplier_id = form.supplier_id.data
        embroidery = Embroidery(
            sku_id=sku_id,
            location=location,
            reorder_point=reorder_point,
            demand=demand,
            total_quantity=total_quantity,
            color=color,
        )
        db.session.add(embroidery)
        db.session.commit()
        product_supplier = ProductSupplier(
            product_id=embroidery.id,
            product_sku_id=embroidery.sku_id,
            supplier_id=supplier_id,
        )
        db.session.add(product_supplier)
        db.session.commit()
        flash("You have successfully added the Product", "success")
        return redirect(url_for('view_embroidery'))
    return render_template("add_embroidery.html", title="Add Embroidery", form=form, add_embroidery=True)


@app.route("/products/raw/htp/add", methods=["GET", "POST"])
def add_htp():
    form = AddHtpForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        location = form.location.data
        reorder_point = form.reorder_point.data
        demand = form.demand.data
        total_quantity = form.total_quantity.data
        supplier_id = form.supplier_id.data
        htp = Htp(
            sku_id=sku_id,
            location=location,
            reorder_point=reorder_point,
            demand=demand,
            total_quantity=total_quantity,
        )
        db.session.add(htp)
        db.session.commit()
        product_supplier = ProductSupplier(
            product_id=htp.id,
            product_sku_id=htp.sku_id,
            supplier_id=supplier_id,
        )
        db.session.add(product_supplier)
        db.session.commit()
        flash("You have successfully added the Product", "success")
        return redirect(url_for('view_htp'))
    return render_template("add_htp.html", title="Add HTP", form=form, add_htp=True)


@app.route("/products/raw/plain_clothing/increase", methods=["GET", "POST"])
def increase_plain_clothing():
    form = UpdatePlainClothingForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = int(form.add_quantity.data)
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=sku_id).first()
        if plain_clothing:
            old_quantity = plain_clothing.total_quantity
            new_quantity = old_quantity + add_quantity
            plain_clothing.total_quantity = new_quantity
            plain_clothing.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_plain_clothing_response.html", title="Updated Plain Clothing Quantity", data=plain_clothing)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("plain_clothing"))
    return render_template("increase_raw_product_request.html", title="Update Plain Clothing Quantity", form=form)


@app.route("/products/raw/htp/increase", methods=["GET", "POST"])
def increase_htp():
    form = UpdateHtpForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = int(form.add_quantity.data)
        htp = Htp.query.filter_by(
            sku_id=sku_id).first()
        if htp:
            old_quantity = htp.total_quantity
            new_quantity = old_quantity + add_quantity
            htp.total_quantity = new_quantity
            htp.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_htp_response.html",  title="Updated HTP Quantity", data=htp)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("htp"))
    return render_template("increase_raw_product_request.html", title="Update HTP Quantity", form=form)


@app.route("/products/raw/embroidery/increase", methods=["GET", "POST"])
def increase_embroidery():
    form = UpdateEmbroideryForm()
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = int(form.add_quantity.data)
        embroidery = Embroidery.query.filter_by(
            sku_id=sku_id).first()
        if embroidery:
            old_quantity = embroidery.total_quantity
            new_quantity = old_quantity + add_quantity
            embroidery.total_quantity = new_quantity
            embroidery.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_embroidery_response.html",  title="Updated Embroidery Quantity", data=embroidery)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("embroidery"))
    return render_template("increase_raw_product_request.html", title="Update Embroidery Quantity", form=form)


@app.route("/products/incoming/delete", methods=["POST"])
def delete_incoming_product():
    sku_id = request.form.get('sku_id')
    incoming_product = IncomingProduct.query.filter_by(sku_id=sku_id).first()
    if incoming_product is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("incoming_products"))
    product_supplier = ProductSupplier.query.filter_by(
        product_sku_id=sku_id).first()
    if product_supplier:
        db.session.delete(product_supplier)
        db.session.commit()
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

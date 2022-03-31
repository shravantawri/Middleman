from random import randint
import datetime
import os
from application import app, models, db, utils
from flask import render_template, request, json, Response, jsonify, redirect, flash, url_for
from application.models import User, Enrollment, Supplier, IncomingProduct, ProductSupplier, PlainClothing, Embroidery, Htp, DesignClothing, DesignImprintedHtp
from application.forms import RegistrationForm, SupplierForm, AddPlainClothingForm, IncreasePlainClothingForm, AddPlainClothingForm, AddEmbroideryForm, AddHtpForm, IncreaseEmbroideryForm, IncreaseHtpForm, UpdateHtpLocationForm, UpdateEmbroideryLocationForm
from application.forms import DecreasePlainClothingForm, DecreaseHtpForm, DecreaseEmbroideryForm, AddDesignImprintedHtpForm, AddDesignedClothingForm, DecreaseDesignedClothingForm, DecreaseDesignImprintedHtpForm, UpdatePlainClothingLocationForm
from werkzeug.utils import secure_filename


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/products/raw/htp/<sku_id>")
def get_htp(sku_id):
    try:
        htp = Htp.query.filter_by(sku_id=sku_id)
        return render_template("htp.html", htpData=htp, view=True, title="HTP")
    except Exception as e:
        flash(f"Oops! No Item present for {sku_id}", "danger")
        return redirect(url_for("view_htp"))


@app.route("/products/raw/plain_clothing/<sku_id>")
def get_plain_clothing(sku_id):
    try:
        plain_clothing = PlainClothing.query.filter_by(sku_id=sku_id)
        return render_template("plain_clothing.html", plainClothingData=plain_clothing, view=True, title="Plain Clothing")
    except Exception as e:
        flash(f"Oops! No Item present for {sku_id}", "danger")
        return redirect(url_for("view_plain_clothing"))


@app.route("/products/raw/embroidery/<sku_id>")
def get_embroidery(sku_id):
    try:
        embroidery = Embroidery.query.filter_by(sku_id=sku_id)
        return render_template("embroidery.html", embroideryData=embroidery, view=True, title="Embroidery")
    except Exception as e:
        flash(f"Oops! No Item present for {sku_id}", "danger")
        return redirect(url_for("view_embroidery"))


@app.route("/qr_code/<raw_item>/<sku_id>", methods=['GET'])
def get_qr_code(raw_item, sku_id):
    # Import QRCode from pyqrcode
    import pyqrcode
    import png
    from pyqrcode import QRCode

    # Generate QR code
    value = 'http://127.0.0.1:5000/products/raw/'+raw_item+'/'+sku_id
    url = pyqrcode.create(value)

    # Create and save the svg file naming "myqr.svg"
    # url.svg("myqr.svg", scale=8)

    # Create and save the png file naming "myqr.png"
    url.png(os.path.join(
        app.config['QR_CODE_FOLDER'], sku_id + '.png'), scale=6)
    # buffer = io.BytesIO()
    # url.png(buffer)

    # print(list(buffer.getvalue()))

    return redirect(url_for('static', filename='images/'+sku_id + '.png'), code=301)


@app.route("/products/raw")
def raw_products():
    return render_template("raw_products.html", raw_products=True)


@app.route("/products/end")
def end_products():
    return render_template("end_products.html", end_products=True)


@app.route("/products/end/designed_clothing")
def view_designed_clothing():
    designed_clothing_data = DesignClothing.query.order_by(
        DesignClothing.updated_at.desc()).all()

    return render_template("designed_clothing.html", designedClothingData=designed_clothing_data, view=True, title="Designed Clothing")


@app.route("/products/end/design_imprinted_htp")
def view_design_imprinted_htp():
    design_imprinted_htp_data = DesignImprintedHtp.query.order_by(
        DesignImprintedHtp.updated_at.desc()).all()

    return render_template("design_imprinted_htp.html", designImprintedHtpData=design_imprinted_htp_data, view=True, title="Design Imprinted HTP")


@app.route("/products/raw/plain_clothing")
def view_plain_clothing():
    plain_clothing_data = PlainClothing.query.filter(PlainClothing.total_quantity > 0).order_by(
        PlainClothing.updated_at.desc())

    return render_template("plain_clothing.html", plainClothingData=plain_clothing_data, view=True, title="Plain Clothing")


@app.route("/products/raw/embroidery")
def view_embroidery():
    embroidery_data = Embroidery.query.filter(Embroidery.total_quantity > 0).order_by(
        Embroidery.updated_at.desc()).all()

    return render_template("embroidery.html", embroideryData=embroidery_data, view=True, title="Embroidery")


@app.route("/products/raw/htp")
def view_htp():
    htp_data = Htp.query.filter(Htp.total_quantity > 0).order_by(
        Htp.updated_at.desc()).all()

    return render_template("htp.html", htpData=htp_data, view=True, title="HTP")


@app.route("/products/raw/plain_clothing/top_sku")
def view_plain_clothing_top_skus():
    plain_clothing_data = PlainClothing.query.order_by(
        PlainClothing.quantity_debit_count.desc()).all()

    return render_template("plain_clothing.html", plainClothingData=plain_clothing_data, top_sku=True, title="Plain Clothing Top SKUs")


@app.route("/products/raw/embroidery/top_sku")
def view_embroidery_top_skus():
    embroidery_data = Embroidery.query.order_by(
        Embroidery.quantity_debit_count.desc()).all()

    return render_template("embroidery.html", embroideryData=embroidery_data, top_sku=True, title="Embroidery Top SKUs")


@app.route("/products/raw/htp/top_sku")
def view_htp_top_skus():
    htp_data = Htp.query.order_by(
        Htp.quantity_debit_count.desc()).all()

    return render_template("htp.html", htpData=htp_data, top_sku=True, title="HTP Top SKUs")


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
@app.route("/products/raw/plain_clothing/<sku_id>/increase", methods=["GET", "POST"])
def increase_plain_clothing(sku_id=None):
    form = IncreasePlainClothingForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = form.add_quantity.data
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
            return redirect(url_for("view_plain_clothing"))
    return render_template("increase_raw_product_request.html", title="Update Plain Clothing Quantity", form=form)


@app.route("/products/raw/htp/increase", methods=["GET", "POST"])
@app.route("/products/raw/htp/<sku_id>/increase", methods=["GET", "POST"])
def increase_htp(sku_id=None):
    form = IncreaseHtpForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = form.add_quantity.data
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
@app.route("/products/raw/embroidery/<sku_id>/increase", methods=["GET", "POST"])
def increase_embroidery(sku_id=None):
    form = IncreaseEmbroideryForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        add_quantity = form.add_quantity.data
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


@app.route("/products/raw/htp/delete", methods=["POST"])
def delete_htp():
    sku_id = request.form.get('sku_id')
    htp = Htp.query.filter_by(sku_id=sku_id).first()
    if htp is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("view_htp"))
    db.session.delete(htp)
    db.session.commit()
    flash(f"Deleted HTP for {sku_id}", "success")
    return redirect(url_for("view_htp"))


@app.route("/products/raw/plain_clothing/delete", methods=["POST"])
def delete_plain_clothing():
    sku_id = request.form.get('sku_id')
    plain_clothing = PlainClothing.query.filter_by(sku_id=sku_id).first()
    if plain_clothing is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("view_plain_clothing"))
    db.session.delete(plain_clothing)
    db.session.commit()
    flash(f"Deleted Plain Clothing for {sku_id}", "success")
    return redirect(url_for("view_plain_clothing"))


@app.route("/products/raw/embroidery/delete", methods=["POST"])
def delete_embroidery():
    sku_id = request.form.get('sku_id')
    embroidery = Embroidery.query.filter_by(sku_id=sku_id).first()
    if embroidery is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("view_embroidery"))
    db.session.delete(embroidery)
    db.session.commit()
    flash(f"Deleted Embroidery for {sku_id}", "success")
    return redirect(url_for("view_embroidery"))


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
def supplier():
    supplier_data = Supplier.query.all()

    return render_template("supplier.html", supplierData=supplier_data, supplier=True)


@app.route("/products/raw/plain_clothing/decrease", methods=["GET", "POST"])
@app.route("/products/raw/plain_clothing/<sku_id>/decrease", methods=["GET", "POST"])
def decrease_plain_clothing(sku_id=None):
    form = DecreasePlainClothingForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        delete_quantity = form.delete_quantity.data
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=sku_id).first()
        if plain_clothing:
            old_quantity = plain_clothing.total_quantity
            new_quantity = old_quantity - delete_quantity
            plain_clothing.total_quantity = new_quantity
            plain_clothing.quantity_debit_count += delete_quantity
            plain_clothing.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_plain_clothing_response.html", title="Updated Plain Clothing Quantity", data=plain_clothing)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_plain_clothing"))
    return render_template("decrease_raw_product_request.html", title="Update Plain Clothing Quantity", form=form)


@app.route("/products/raw/htp/decrease", methods=["GET", "POST"])
@app.route("/products/raw/htp/<sku_id>/decrease", methods=["GET", "POST"])
def decrease_htp(sku_id=None):
    form = DecreaseHtpForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        delete_quantity = form.delete_quantity.data
        htp = Htp.query.filter_by(
            sku_id=sku_id).first()
        if htp:
            old_quantity = htp.total_quantity
            new_quantity = old_quantity - delete_quantity
            htp.total_quantity = new_quantity
            htp.quantity_debit_count += delete_quantity
            htp.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_htp_response.html",  title="Updated HTP Quantity", data=htp)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("htp"))
    return render_template("decrease_raw_product_request.html", title="Update HTP Quantity", form=form)


@app.route("/products/raw/embroidery/decrease", methods=["GET", "POST"])
@app.route("/products/raw/embroidery/<sku_id>/decrease", methods=["GET", "POST"])
def decrease_embroidery(sku_id=None):
    form = DecreaseEmbroideryForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        delete_quantity = form.delete_quantity.data
        embroidery = Embroidery.query.filter_by(
            sku_id=sku_id).first()
        if embroidery:
            old_quantity = embroidery.total_quantity
            new_quantity = old_quantity - delete_quantity
            embroidery.total_quantity = new_quantity
            embroidery.quantity_debit_count += delete_quantity
            embroidery.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_embroidery_response.html",  title="Updated Embroidery Quantity", data=embroidery)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("embroidery"))
    return render_template("decrease_raw_product_request.html", title="Update Embroidery Quantity", form=form)


@app.route("/products/end/design_imprinted_htp/add", methods=["GET", "POST"])
def add_design_imprinted_htp():
    form = AddDesignImprintedHtpForm()
    if form.validate_on_submit():
        location = form.location.data
        category = form.category.data
        total_quantity = form.total_quantity.data
        design_code = form.design_code.data
        sku_id = utils.generate_sku_id(category, design_code)
        design_imprinted_htp = DesignImprintedHtp(
            sku_id=sku_id,
            location=location,
            category=category,
            total_quantity=total_quantity,
        )
        db.session.add(design_imprinted_htp)
        db.session.commit()
        flash(
            f'You have successfully created Design Imprinted HTP with SKU ID: {sku_id}', "success")
        return redirect(url_for('view_design_imprinted_htp'))
    return render_template("add_design_imprinted_htp.html", title="Create Design Imprinted HTP", form=form, add_htp=True)


@app.route("/products/end/designed_clothing/add", methods=["GET", "POST"])
def add_designed_clothing():
    form = AddDesignedClothingForm()
    if form.validate_on_submit():
        location = form.location.data
        total_quantity = form.total_quantity.data
        color = form.color.data
        material = form.material.data
        sleeve_type = form.sleeve_type.data
        size = form.size.data
        category = form.category.data
        design_code = form.design_code.data
        f = form.image.data
        image_url = utils.upload_image_to_bucket(f)
        sku_id = utils.generate_sku_id(category, design_code)
        designed_clothing = DesignClothing(
            sku_id=sku_id,
            location=location,
            total_quantity=total_quantity,
            color=color,
            sleeve_type=sleeve_type,
            material=material,
            size=size,
            category=category,
            image_url=image_url
        )
        db.session.add(designed_clothing)
        db.session.commit()
        flash(
            f'You have successfully created Designed Clothing with SKU ID: {sku_id}', "success")
        return redirect(url_for('view_designed_clothing'))
    return render_template("add_designed_clothing.html", title="Create Designed Clothing", form=form, add_plain_clothing=True)


@app.route("/products/end/designed_clothing/top_sku")
def view_designed_clothing_top_skus():
    design_clothing_data = DesignClothing.query.order_by(
        DesignClothing.quantity_debit_count.desc()).all()

    return render_template("designed_clothing.html", designedClothingData=design_clothing_data, top_sku=True, title="Designed Clothing Top SKUs")


@app.route("/products/end/design_imprinted_htp/top_sku")
def view_design_imprinted_htp_top_skus():
    design_imprinted_htp_data = DesignImprintedHtp.query.order_by(
        DesignImprintedHtp.quantity_debit_count.desc()).all()

    return render_template("design_imprinted_htp.html", designImprintedHtpData=design_imprinted_htp_data, top_sku=True, title="Design Imprinted HTP Top SKUs")


@app.route("/products/end/designed_clothing/decrease", methods=["GET", "POST"])
@app.route("/products/end/designed_clothing/<sku_id>/decrease", methods=["GET", "POST"])
def decrease_designed_clothing(sku_id=None):
    form = DecreaseDesignedClothingForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        delete_quantity = form.delete_quantity.data
        customer_name = form.customer_name.data
        designed_clothing = DesignClothing.query.filter_by(
            sku_id=sku_id).first()
        if designed_clothing:
            old_quantity = designed_clothing.total_quantity
            new_quantity = old_quantity - delete_quantity
            designed_clothing.total_quantity = new_quantity
            designed_clothing.quantity_debit_count += delete_quantity
            designed_clothing.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_designed_clothing_response.html", title="Shiped Designed Clothing", data=designed_clothing)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_designed_clothing"))
    return render_template("ship_end_product_request.html", title="Ship Designed Clothing", form=form)


@app.route("/products/end/design_imprinted_htp/decrease", methods=["GET", "POST"])
@app.route("/products/end/design_imprinted_htp/<sku_id>/decrease", methods=["GET", "POST"])
def decrease_design_imprinted_htp(sku_id=None):
    form = DecreaseDesignImprintedHtpForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        delete_quantity = form.delete_quantity.data
        customer_name = form.customer_name.data
        design_imprinted_htp = DesignImprintedHtp.query.filter_by(
            sku_id=sku_id).first()
        if design_imprinted_htp:
            old_quantity = design_imprinted_htp.total_quantity
            new_quantity = old_quantity - delete_quantity
            design_imprinted_htp.total_quantity = new_quantity
            design_imprinted_htp.quantity_debit_count += delete_quantity
            design_imprinted_htp.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated quantity of product: {sku_id} from: {old_quantity} to: {new_quantity}", "success")
            return render_template("update_design_imprinted_htp_response.html", title="Shiped Design Imprinted HTP", data=design_imprinted_htp)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_design_imprinted_htp"))
    return render_template("ship_end_product_request.html", title="Ship Design Imprinted HTP", form=form)


@app.route("/products/end/design_imprinted_htp/delete", methods=["POST"])
def delete_design_imprinted_htp():
    sku_id = request.form.get('sku_id')
    htp = DesignImprintedHtp.query.filter_by(sku_id=sku_id).first()
    if htp is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("view_design_imprinted_htp"))
    db.session.delete(htp)
    db.session.commit()
    flash(f"Deleted Design Imprinted HTP for {sku_id}", "success")
    return redirect(url_for("view_design_imprinted_htp"))


@app.route("/products/end/designed_clothing/delete", methods=["POST"])
def delete_designed_clothing():
    sku_id = request.form.get('sku_id')
    designed_clothing = DesignClothing.query.filter_by(sku_id=sku_id).first()
    if designed_clothing is None:
        flash(f"Oops! No Product present for {sku_id}", "danger")
        return redirect(url_for("view_designed_clothing"))
    db.session.delete(designed_clothing)
    db.session.commit()
    flash(f"Deleted Designed Clothing for {sku_id}", "success")
    return redirect(url_for("view_designed_clothing"))


@app.route("/products/raw/plain_clothing/<sku_id>/update", methods=["GET", "POST"])
def update_plain_clothing_location(sku_id=None):
    form = UpdatePlainClothingLocationForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        new_location = form.location.data
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=sku_id).first()
        if plain_clothing:
            old_location = plain_clothing.location
            plain_clothing.location = new_location
            plain_clothing.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated location of product: {sku_id} from: {old_location} to: {new_location}", "success")
            return render_template("update_plain_clothing_response.html", title="Updated Plain Clothing Quantity", data=plain_clothing)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_plain_clothing"))
    return render_template("update_raw_product_location_request.html", title="Update Plain Clothing Location", form=form)


@app.route("/products/raw/htp/<sku_id>/update", methods=["GET", "POST"])
def update_htp_location(sku_id=None):
    form = UpdateHtpLocationForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        new_location = form.location.data
        htp = Htp.query.filter_by(
            sku_id=sku_id).first()
        if htp:
            old_location = htp.location
            htp.location = new_location
            htp.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated location of product: {sku_id} from: {old_location} to: {new_location}", "success")
            return render_template("update_htp_response.html", title="Updated HTP Quantity", data=htp)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_htp"))
    return render_template("update_raw_product_location_request.html", title="Update HTP Location", form=form)


@app.route("/products/raw/embroidery/<sku_id>/update", methods=["GET", "POST"])
def update_embroidery_location(sku_id=None):
    form = UpdateEmbroideryLocationForm()
    if sku_id:
        form.sku_id.data = sku_id
    if form.validate_on_submit():
        sku_id = form.sku_id.data
        new_location = form.location.data
        embroidery = Embroidery.query.filter_by(
            sku_id=sku_id).first()
        if embroidery:
            old_location = embroidery.location
            embroidery.location = new_location
            embroidery.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            flash(
                f"Updated location of product: {sku_id} from: {old_location} to: {new_location}", "success")
            return render_template("update_embroidery_response.html", title="Updated Embroidery Quantity", data=embroidery)
        else:
            flash(f"Oops! No Item present for {sku_id}", "danger")
            return redirect(url_for("view_embroidery"))
    return render_template("update_raw_product_location_request.html", title="Update Embroidery Location", form=form)

from application import app, models, db
from flask import render_template, request, json, Response, jsonify, redirect, flash, url_for
from application.models import User, RawItem, Enrollment
from application.forms import LoginForm, RegistrationForm

import os


@app.route("/")
@app.route("/index")
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

    return render_template("raw_items.html", rawItemData=raw_item_data)


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


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if (idx == None):
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]

#     return Response(json.dumps(jdata), mimetype="application/json")


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

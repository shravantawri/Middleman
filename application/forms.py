from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User, Supplier, IncomingProduct, ProductSupplier


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[
                           DataRequired(), Length(min=6, max=15)])
    password_confirm = StringField(
        "Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name ", validators=[
                             DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(min=2, max=55)])
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use!")


class SupplierForm(FlaskForm):
    id = StringField("Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    lead_time = StringField("Lead Time", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_id(self, id):
        supplier = Supplier.query.filter_by(id=id.data).first()
        if supplier:
            raise ValidationError("Id is already in use!")


class IncomingProductForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    reorder_point = StringField("Reorder Point", validators=[DataRequired()])
    demand = StringField("Demand", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    supplier_id = StringField("Supplier Id", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_sku_id(self, sku_id):
        incoming_product = IncomingProduct.query.filter_by(
            sku_id=sku_id.data).first()
        if incoming_product:
            raise ValidationError("SKU Id is already in use!")

    def validate_supplier_id(self, supplier_id):
        supplier = Supplier.query.filter_by(
            id=supplier_id.data).first()
        if not supplier:
            raise ValidationError(
                "Supplier not present for this particular ID")

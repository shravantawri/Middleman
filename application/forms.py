from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User, RawItem


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[
                           DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Rememeber Me")
    submit = SubmitField("Login")


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


class ItemForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    colour = StringField(
        "colour", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_sku_id(self, sku_id):
        raw_item = RawItem.query.filter_by(sku_id=sku_id.data).first()
        if raw_item:
            raise ValidationError("SKU Id is already in use!")

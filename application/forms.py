from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User, Supplier, IncomingProduct, ProductSupplier, PlainClothing, Htp, Embroidery, DesignClothing, DesignImprintedHtp
from flask_wtf.file import FileField, FileRequired


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
    lead_time = IntegerField("Lead Time", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_id(self, id):
        supplier = Supplier.query.filter_by(id=id.data).first()
        if supplier:
            raise ValidationError("Id is already in use!")


class AddPlainClothingForm(FlaskForm):
    color_list = ['Black', 'Charcoal', 'Navy', 'Sports Grey']
    size_list = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    material_list = ['SweatShirt', 'Full Zip Hooded SweatShirt',
                     'Hooded Swearshirt', 'Cotton t-shirt']
    sleeve_type_list = ['Full Sleeve', 'Half Sleeve']
    sku_id = StringField("SKU ID", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    reorder_point = StringField("Reorder Point", validators=[DataRequired()])
    demand = StringField("Demand", validators=[DataRequired()])
    total_quantity = StringField("Total Quantity", validators=[DataRequired()])
    color = SelectField("Colour", choices=color_list,
                        validators=[DataRequired()])
    material = SelectField(
        "Material", choices=material_list, validators=[DataRequired()])
    sleeve_type = SelectField(
        "Sleeve Type", choices=sleeve_type_list, validators=[DataRequired()])
    size = SelectField("Size", choices=size_list, validators=[DataRequired()])
    supplier_id = StringField("Supplier Id", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_sku_id(self, sku_id):
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=sku_id.data).first()
        if plain_clothing:
            raise ValidationError("SKU Id is already in use!")

    def validate_supplier_id(self, supplier_id):
        supplier = Supplier.query.filter_by(
            id=supplier_id.data).first()
        if not supplier:
            raise ValidationError(
                "Supplier not present for this particular ID")


class AddEmbroideryForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    reorder_point = StringField("Reorder Point", validators=[DataRequired()])
    demand = StringField("Demand", validators=[DataRequired()])
    total_quantity = StringField("Total Quantity", validators=[DataRequired()])
    color = StringField("Colour", validators=[DataRequired()])
    supplier_id = StringField("Supplier Id", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_sku_id(self, sku_id):
        embroidery = Embroidery.query.filter_by(
            sku_id=sku_id.data).first()
        if embroidery:
            raise ValidationError("SKU Id is already in use!")

    def validate_supplier_id(self, supplier_id):
        supplier = Supplier.query.filter_by(
            id=supplier_id.data).first()
        if not supplier:
            raise ValidationError(
                "Supplier not present for this particular ID")


class AddHtpForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    reorder_point = StringField("Reorder Point", validators=[DataRequired()])
    demand = StringField("Demand", validators=[DataRequired()])
    total_quantity = StringField("Total Quantity", validators=[DataRequired()])
    supplier_id = StringField("Supplier Id", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_sku_id(self, sku_id):
        htp = Htp.query.filter_by(
            sku_id=sku_id.data).first()
        if htp:
            raise ValidationError("SKU Id is already in use!")

    def validate_supplier_id(self, supplier_id):
        supplier = Supplier.query.filter_by(
            id=supplier_id.data).first()
        if not supplier:
            raise ValidationError(
                "Supplier not present for this particular ID")


class IncreasePlainClothingForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    add_quantity = IntegerField("Add Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_sku_id(self, sku_id):
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=sku_id.data).first()
        if not plain_clothing:
            raise ValidationError(
                f'Product for SKU ID: {sku_id.data} is not present. Please add plain clothing')


class IncreaseHtpForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    add_quantity = IntegerField("Add Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_sku_id(self, sku_id):
        htp = Htp.query.filter_by(
            sku_id=sku_id.data).first()
        if not htp:
            raise ValidationError(
                f'Product for SKU ID: {sku_id.data} is not present. Please add HTP')


class IncreaseEmbroideryForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    add_quantity = IntegerField("Add Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_sku_id(self, sku_id):
        embroidery = Embroidery.query.filter_by(
            sku_id=sku_id.data).first()
        if not embroidery:
            raise ValidationError(
                f'Product for SKU ID: {sku_id.data} is not present. Please add embroidery')


class DecreasePlainClothingForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    delete_quantity = IntegerField(
        "Delete Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not plain_clothing:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please add plain clothing')
            return False
        if plain_clothing.total_quantity < self.delete_quantity.data:
            self.delete_quantity.errors.append(
                f'Product for SKU ID: {self.sku_id.data}, only {plain_clothing.total_quantity} units are available')
            return False
        return result


class DecreaseHtpForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    delete_quantity = IntegerField(
        "Delete Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        htp = Htp.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not htp:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please add htp')
            return False
        if htp.total_quantity < self.delete_quantity.data:
            self.delete_quantity.errors.append(
                f'Product for SKU ID: {self.sku_id.data}, only {htp.total_quantity} units are available')
            return False
        return result


class DecreaseEmbroideryForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    delete_quantity = IntegerField(
        "Delete Quantity", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        embroidery = Embroidery.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not embroidery:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please add embroidery')
            return False
        if embroidery.total_quantity < self.delete_quantity.data:
            self.delete_quantity.errors.append(
                f'Product for SKU ID: {self.sku_id.data}, only {embroidery.total_quantity} units are available')
            return False
        return result


class AddDesignImprintedHtpForm(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    total_quantity = StringField("Total Quantity", validators=[DataRequired()])
    design_code = StringField("Design Code")

    submit = SubmitField("Create")


class AddDesignedClothingForm(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    total_quantity = StringField("Total Quantity", validators=[DataRequired()])
    color = StringField("Colour", validators=[DataRequired()])
    material = StringField("Material", validators=[DataRequired()])
    sleeve_type = StringField("Sleeve Type", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired()])
    design_code = StringField("Design Code")

    submit = SubmitField("Add")


class DecreaseDesignedClothingForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    delete_quantity = IntegerField(
        "Delete Quantity", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        designed_clothing = DesignClothing.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not designed_clothing:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please create designed clothing')
            return False
        if designed_clothing.total_quantity < self.delete_quantity.data:
            self.delete_quantity.errors.append(
                f'Product for SKU ID: {self.sku_id.data}, only {designed_clothing.total_quantity} units are available')
            return False
        return result


class DecreaseDesignImprintedHtpForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    delete_quantity = IntegerField(
        "Delete Quantity", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        design_imprinted_htp = DesignImprintedHtp.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not design_imprinted_htp:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please create Design Imprinted HTP')
            return False
        if design_imprinted_htp.total_quantity < self.delete_quantity.data:
            self.delete_quantity.errors.append(
                f'Product for SKU ID: {self.sku_id.data}, only {design_imprinted_htp.total_quantity} units are available')
            return False
        return result


class UpdatePlainClothingLocationForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        plain_clothing = PlainClothing.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not plain_clothing:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please create Plain Clothing')
            return False
        return result


class UpdateHtpLocationForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        htp = Htp.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not htp:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please create HTP')
            return False
        return result


class UpdateEmbroideryLocationForm(FlaskForm):
    sku_id = StringField("SKU Id", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        embroidery = Embroidery.query.filter_by(
            sku_id=self.sku_id.data).first()
        if not embroidery:
            self.sku_id.errors.append(
                f'Product for SKU ID: {self.sku_id.data} is not present. Please create Embroidery')
            return False
        return result

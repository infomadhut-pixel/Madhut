import re

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from ..Schemas.Admin.tshirt_upload import ProductSchema
from app.extensions import socketio

product_bp = Blueprint('product', __name__)


def generate_slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@product_bp.route('/admin/add-product')
class add_product(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()

    # @jwt_required(locations=['headers'])
    def post(self):
        from ..Config.cloudinary import cloudinary
        schema = ProductSchema()
        form_data = request.form.to_dict(flat=False)

        # Fix single-value fields (they come as list, but schema expects single value)
        form_data["name"] = request.form.get("name")
        form_data["description"] = request.form.get("description")
        form_data["price"] = request.form.get("price")
        form_data["old_price"] = request.form.get("old_price")
        form_data["stock"] = request.form.get("stock")
        form_data["category"] = request.form.get("category")

        # Ensure list fields always remain list
        form_data["sizes"] = request.form.getlist("sizes")
        form_data["colors"] = request.form.getlist("colors")
        form_data["tags"] = request.form.getlist("tags")
        try:
            data = schema.load(form_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
        price = data['price']
        old_price = data.get('old_price', 0)
        discount = 0
        if old_price and old_price > 0:
            discount = int(((old_price - price) / old_price) * 100)
        files = request.files.getlist('images')
        if len(files) == 0:
            return jsonify({'error': 'Minimum 1 image required'}), 400
        if len(files) > 5:
            return jsonify({'error': 'Maximum 5 image allowed'}), 400

        images_urls = []
        for file in files:
            filename = secure_filename(file.filename)
            if filename == '':
                return jsonify({"error": "Invalid file"}), 400
            if not allowed_file(filename):
                return jsonify({"error": "Only JPG and PNG allowed"}), 400
            upload_result = cloudinary.uploader.upload(file)
            images_urls.append(upload_result['secure_url'])
        name = data['name']
        description = data['description']
        price = data['price']
        old_price = data['old_price']
        images = images_urls
        size = data['sizes']
        colors = data['colors']
        stock = data['stock']
        category = data['category']
        tags = data['tags']
        slug = generate_slug(data['name'])
        discount_percent = discount
        product = self.product_db.insert_data(name, description, price, old_price, images, size, colors, stock, category,
                                             tags, slug, discount_percent)
        socketio.emit("new_product", product)

        return {
            "message": "Product added successfully",
            "success": True,
            "product": product
        }, 201

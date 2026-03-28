from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from ..authorise import get_current_user
from ..Database.User.customised_check_out import CustomisedProductDatabase

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


blp = Blueprint('customised order store', __name__)


@blp.route('/user/order/customised/product')
class CustomisedProduct(MethodView):
    def __init__(self):
        self.product_db = CustomisedProductDatabase()

    def post(self):
        from ..Config.cloudinary import cloudinary
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401
        payment_method = request.form.get("payment_method")
        delivery_charge = request.form.get("delivery_charge")

        file = request.files.get("image")
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result['secure_url']
        color = request.form.get("color")
        size = request.form.get("size")
        price = int(request.form.get("price", 0))
        quantity = int(request.form.get("quantity", 0))

        full_name = request.form.get("fullName")
        phone = request.form.get("phone")
        address = request.form.get("address")
        city = request.form.get("city")
        pincode = request.form.get("pincode")

        result = self.product_db.store_customised_checkout_order(email, full_name, phone, address, city, pincode,
                                                                 image_url, color, size, price, quantity,
                                                                 payment_method, delivery_charge)
        return result

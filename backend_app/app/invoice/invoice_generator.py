import logging

from flask import request, send_file
from flask_smorest import Blueprint
from flask.views import MethodView

from ..Database.User.check_out import OrderTshirt
from ..authorise import get_current_user
from .pdf_service import generate_invoice_pdf

blp = Blueprint("user invoice", __name__)


@blp.route("/generate/invoice/of/order")
class CheckOutOrder(MethodView):

    def __init__(self):
        self.order_db = OrderTshirt()

    def post(self):
        # 1. Authenticate the user.
        email = get_current_user()

        if not email or not isinstance(email, str):
            return {"message": "Unauthorized"}, 401

        # 2. Validate the request.
        data = request.get_json()
        order_id = data.get("order_id")

        if not isinstance(order_id, str) or not order_id.strip():
            return {"message": "order_id is required"}, 400

        order_id = order_id.strip()

        # 3. Fetch the selected order.
        order = self.order_db.find_order(order_id)

        if not order:
            return {"message": "Order not found"}, 404

        if not isinstance(order, dict):
            return {"message": "Invalid order data"}, 500

        # 4. Verify that the order belongs to this user.
        order_email = order.get("user_email")

        if (
                not isinstance(order_email, str)
                or email.strip().lower() != order_email.strip().lower()
        ):
            return {
                "message": (
                    "You are not authorized to access this order's invoice."
                )
            }, 403

        # 5. Generate the PDF only after ownership verification.
        try:
            pdf_buffer = generate_invoice_pdf(order)

            return send_file(
                pdf_buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"MadHut-Invoice-{order_id}.pdf",
            )

        except Exception:
            logging.exception("MadHut invoice PDF generation failed")
            return {
                "message": "Unable to generate invoice. Please try again."
            }, 500

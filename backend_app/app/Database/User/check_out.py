from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

import random


def generate_order_id():
    return "MH" + datetime.utcnow().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))


class OrderTshirt:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['tshirt-order']

    def create_order_index(self):
        self.collection.create_index("order_id", unique=True)
        self.collection.create_index("user_id")
        self.collection.create_index("order_status")
        self.collection.create_index("created_at")
        self.collection.create_index("payment_status")

    def create_order(self, user_email, data):
        product_id = ObjectId(data["product_id"])
        quantity = int(data["quantity"])
        price = float(data["price"])

        subtotal = quantity * price

        order_data = {
            "order_id": generate_order_id(),
            "user_email": user_email,

            "items": [
                {
                    "product_id": product_id,
                    "name": data["name"],
                    "image": data["image"],
                    "size": data["size"],
                    "color": data["color"],
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                }
            ],

            "total_amount": subtotal,

            "shipping_address": {
                "full_name": data["full_name"],
                "phone": data["phone"],
                "address": data["address"],
                "city": data["city"],
                "pincode": data["pincode"]
            },

            "payment_mode": data["payment_mode"],
            "payment_status": "pending",
            "order_status": "placed",

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self.collection.insert_one(order_data)
        return {"success": True, "order_id": order_data["order_id"]}

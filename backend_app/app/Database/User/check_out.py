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
        self.collection.create_index("email")
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
            "order_status": "pending",
            'tracking_id': None,

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            'is_reviewed': False
        }
        self.collection.insert_one(order_data)
        return {"success": True, "order_id": order_data["order_id"]}

    def fetch_all_order(self, email):
        order_data = self.collection.find({'user_email': email}).sort("created_at", -1)
        order_data_list = []
        for order in order_data:
            order['_id'] = str(order.get("_id"))
            order['items'][0]['product_id'] = str(order['items'][0]["product_id"])
            order_data_list.append(order)
        return order_data_list

    def fetch_order(self, skip=0, limit=5):
        order_data = self.collection.find().sort("created_at", -1).skip(skip).limit(limit)
        order_data_list = []
        for data in order_data:
            data['_id'] = str(data.get("_id"))
            data['items'][0]['product_id'] = str(data['items'][0].get('product_id'))
            order_data_list.append(data)
        return order_data_list

    def update_order_status(self, order_id, order_status):
        try:
            self.collection.update_one({"order_id": order_id}, {
                "$set": {"order_status": order_status}
            })
            return {'message': 'Order status successfully updated...'}, 200
        except Exception as e:
            return {"message": "Unknown error occurred..."}, 500

    def update_tracking_id(self, order_id, tracking_id):
        try:
            self.collection.update_one({"order_id": order_id}, {
                "$set": {"tracking_id": tracking_id}
            })
            return {'message': 'Tracking id successfully updated...'}, 200
        except Exception as e:
            return {"message": "Unknown error occurred..."}, 500

    def update_review_status(self, order_id):
        self.collection.update_one({"order_id": order_id}, {
            "$set": {"is_reviewed": True}
        })

from pymongo import MongoClient
from datetime import datetime
import random
import string


def generate_order_id():
    return "MH" + datetime.utcnow().strftime("%Y%m%d") + \
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


class CustomisedProductDatabase:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['customised_order']

    def store_customised_checkout_order(
            self,
            email,
            fullName,
            phone,
            address,
            city,
            pincode,
            image_url,
            color,
            size,
            price,
            quantity,
            payment_method,
            delivery_total,
    ):
        subtotal = price * quantity

        order_data = {
            "order_id": generate_order_id(),
            "email": email,
            'fullName': fullName,
            'phone': phone,
            'address': address,
            'city': city,
            'pincode': pincode,
            "items": [
                {
                    "type": "customised",
                    "image_url": image_url,
                    "color": color,
                    "size": size,
                    "price": price,
                    "quantity": quantity
                }
            ],
            "subtotal": subtotal,
            "delivery_charge": delivery_total,
            "final_total": subtotal + 0,
            "payment_mode": payment_method,
            "payment_status": "Pending",
            "order_status": "Placed",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = self.collection.insert_one(order_data)
        if result.inserted_id:
            return {'message': 'Order created successfully...'}

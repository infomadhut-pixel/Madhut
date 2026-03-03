from pymongo import MongoClient
from datetime import datetime


class AddToCart:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['add_to_cart']

    def add_to_cart(self, email, product_id, size, color, quantity, price, image):

        try:
            cart = self.collection.find_one({"email": email})

            #  CART EXISTS
            if cart:

                existing_item = next(
                    (item for item in cart["items"]
                     if item["product_id"] == product_id
                     and item["size"] == size
                     and item["color"] == color),
                    None
                )

                #  SAME PRODUCT + SAME VARIANT
                if existing_item:
                    self.collection.update_one(
                        {
                            "email": email,
                            "items.product_id": product_id,
                            "items.size": size,
                            "items.color": color
                        },
                        {
                            "$inc": {
                                "items.$.quantity": quantity,
                                "total_items": quantity
                            },
                            "$set": {"updated_at": datetime.utcnow()}
                        }
                    )

                    return {
                        "message": "Quantity updated successfully"
                    }, 200

                #  NEW VARIANT
                else:
                    self.collection.update_one(
                        {"email": email},
                        {
                            "$push": {
                                "items": {
                                    "product_id": product_id,
                                    "size": size,
                                    "color": color,
                                    "quantity": quantity,
                                    "price_at_added": price,
                                    "image": image,
                                    "added_at": datetime.utcnow()
                                }
                            },
                            "$inc": {"total_items": quantity},
                            "$set": {"updated_at": datetime.utcnow()}
                        }
                    )

                    return {
                        "message": "Product added to cart"
                    }, 201

            #  FIRST TIME CART CREATION
            else:
                self.collection.insert_one({
                    "email": email,
                    "items": [{
                        "product_id": product_id,
                        "size": size,
                        "color": color,
                        "quantity": quantity,
                        "price_at_added": price,
                        "image": image,
                        "added_at": datetime.utcnow()
                    }],
                    "total_items": quantity,
                    "updated_at": datetime.utcnow()
                })

                return {
                    "message": "Cart created and product added"
                }, 201

        except Exception as e:
            return {
                "error": "Failed to add item to cart",
                "details": str(e)
            }, 500

    def number_total_item_add_in_cart(self, email):
        data = self.collection.find_one({'email': email})
        return data['total_items']


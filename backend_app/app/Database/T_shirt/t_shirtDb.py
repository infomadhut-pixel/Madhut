from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import random


class TshirtDatabase:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut',
            tls=True)
        self.db = self.client['MadHut']
        self.collection = self.db['T_shirt']

    def insert_data(self, name, description, price, old_price, images, sizes, colors, stock, category, tags, slug,
                    discount_percent):
        product_data = {'name': name, 'description': description, 'price': price, 'old_price': old_price,
                        'images': images, 'sizes': sizes, 'colors': colors, 'stock': stock, 'category': category,
                        'tags': tags,
                        'slugs': slug, 'discount_percent': discount_percent, 'is_active': True, 'is_featured': False,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow(),
                        'random': random.random()}
        image = images[0]
        result = self.collection.insert_one(product_data)

        return {"_id": str(result.inserted_id), "name": name, 'price': price, "old_price": old_price,
                "image": image}

    def fetch_products(self, last_id=None, limit=20):
        query = {}

        # ✅ handle cursor safely
        if last_id:
            try:
                query["_id"] = {"$lt": ObjectId(last_id)}
            except Exception:
                return {
                    "products": [],
                    "has_more": False,
                    "next_cursor": None,
                    "count": 0
                }

        projection = {
            "name": 1,
            "price": 1,
            "old_price": 1,
            "discount_percent": 1,
            "images": {"$slice": 1}
        }

        cursor = (
            self.collection
            .find(query, projection)
            .sort("_id", -1)
            .limit(limit + 1)
        )

        products = list(cursor)

        has_more = len(products) > limit

        if has_more:
            products = products[:limit]

        # ✅ convert ObjectId → string
        for p in products:
            p["_id"] = str(p["_id"])

        next_cursor = products[-1]["_id"] if products else None

        return {
            "products": products,
            "has_more": has_more,
            "next_cursor": next_cursor,
            "count": len(products)
        }

    def fetch_single_product_detail(self, product_id):
        detail = self.collection.find_one({"_id": ObjectId(product_id)})
        detail["_id"] = str(detail.get('_id'))
        return detail

    def fetch_new_arrival(self, page, limit):
        skip = (page - 1) * limit
        projection = {
            'name': 1,
            'price': 1,
            'old': 1,
            "images": {"$slice": 1}
        }
        datas = (self.collection.find({}, projection).sort("created_at", -1).skip(skip).limit(limit))
        product_list = []
        for data in datas:
            data["_id"] = str(data.get("_id"))
            product_list.append(data)
        return {'products': product_list}

    def update_product_detail(self, project_id, data):
        self.collection.update_one({"_id": ObjectId(project_id)}, {"$set": data})
        return {"message": "Product updated..."}, 200

    def delete_product(self, product_id):
        response = self.collection.delete_one({'_id': ObjectId(product_id)})
        if response.deleted_count > 0:
            return {"message": "Deleted Successfully"}, 200
        else:
            return {"message": "Product not found or some unknown error occurred..."}, 404

    def update_stock(self, product_id, quantity):
        self.collection.update_one(
            {
                "_id": product_id,
                "stock": {"$gte": quantity}
            },
            {"$inc": {'stock': -quantity}}
        )

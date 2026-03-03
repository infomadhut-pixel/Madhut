from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime


class TshirtDatabase:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['T_shirt']

    def insert_data(self, name, description, price, old_price, images, sizes, colors, stock, category, tags, slug,
                    discount_percent):
        product_data = {'name': name, 'description': description, 'price': price, 'old_price': old_price,
                        'images': images, 'sizes': sizes, 'colors': colors, 'stock': stock, 'category': category,
                        'tags': tags,
                        'slugs': slug, 'discount_percent': discount_percent, 'is_active': True, 'is_featured': False,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()}
        result = self.collection.insert_one(product_data)
        product_data['_id'] = str(result.inserted_id)

        return {"message": 'Product added successfully', 'product': product_data}, 201

    def fetch_product(self, page, limit, min_price=None, max_price=None):
        skip = (page - 1) * limit

        query = {}

        if min_price is not None and max_price is not None:
            query['price'] = {'$gte': min_price, '$lte': max_price}

        # 🔥 Only required fields
        projection = {
            "name": 1,
            "price": 1,
            "old_price": 1,
            "images": {"$slice": 1},  # only first image
        }

        datas = (
            self.collection
            .find(query, projection)
            .skip(skip)
            .limit(limit)
        )

        product_list = []

        for data in datas:
            data['_id'] = str(data.get("_id"))
            product_list.append(data)

        total_products = self.collection.count_documents(query)
        total_pages = (total_products + limit - 1) // limit
        return {
            'products': product_list,
            'total_pages': total_pages
        }

    def fetch_single_product_detail(self, product_id):
        detail = self.collection.find_one({"_id": ObjectId(product_id)})
        detail["_id"] = str(detail.get('_id'))
        return detail



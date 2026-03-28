from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime


class Review:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['T_shirt_reviews']
        self.collection.create_index([
            ("product_id", 1),
            ("created_at", -1)
        ])

    def add_reviews(self, product_id, name, star_rating, feedback):
        review_data = {
            "product_id": product_id,
            "name": name.lower(),
            "star_rating": star_rating,
            'feedback': feedback,
            'created_at': datetime.utcnow()
        }
        self.collection.insert_one(review_data)
        return {"message": "Review added successfully", "status": 'success'}, 200

    def get_reviews(self, product_id):
        pipeline = [
            {"$match": {"product_id": product_id}},
            {"$sort": {"created_at": -1}},

            {
                "$group": {
                    "_id": "$name",
                    "name": {"$first": "$name"},
                    "star_rating": {"$first": "$star_rating"},
                    "feedback": {"$first": "$feedback"},
                    "created_at": {"$first": "$created_at"}
                }
            },

            {"$sort": {"created_at": -1}},
            {"$limit": 20}
        ]
        response = self.collection.aggregate(pipeline)
        reviews_list = []

        for doc in response:
            reviews_list.append({
                "name": doc["name"],
                "star_rating": doc["star_rating"],
                "feedback": doc["feedback"],
                'created_at': str(doc.get('created_at'))
            })
        return reviews_list

    def get_all_reviews(self):
        response = self.collection.find().sort({'created_at': -1})
        review_list = []
        for data in response:
            data["_id"] = str(data.get("_id"))
            review_list.append(data)
        return review_list

    def delete_review(self, _id):
        response = self.collection.delete_one({'_id': ObjectId(_id)})
        if response.deleted_count > 0:
            return {"message": "review deleted successfully..."}, 200
        else:
            return {"message": 'some unknown error occurred...'}, 500

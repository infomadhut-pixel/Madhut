from pymongo import MongoClient


class UserAddToCartLog:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['add_to_cart_logs']

    def save_add_tp_cart_log(self, data):
        self.collection.insert_one(data)

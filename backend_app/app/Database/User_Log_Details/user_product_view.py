from pymongo import MongoClient


class ProductViewLog:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['product_view_log']

    def save_product_view_log(self, data):
        self.collection.insert_one(data)

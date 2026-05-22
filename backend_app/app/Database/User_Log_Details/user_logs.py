from pymongo import MongoClient


class SaveUserActivity:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['user_logs_details']

    def save_user_activity(self, activity_data):
        self.collection.insert_one(activity_data)

from pymongo import MongoClient
import uuid
from datetime import datetime

from app.extensions import bcrypt


class UserDatabase:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://harshkumartiwari034_db_user:AEXLTbDqQwSQ9CQ0@madhut.ej8ujxj.mongodb.net/?appName=MadHut')
        self.db = self.client['MadHut']
        self.collection = self.db['user']

    def create_index(self):
        self.collection.create_index('email', unique=True)
        self.collection.create_index('unique_id', unique=True)
        self.collection.create_index('created_at')

    def register_user(self, username, email, contact_number, street, pin_code, country):
        unique_id = uuid.uuid4().hex[:10].upper()

        user_data = {
            'unique_id': unique_id,
            'username': username,
            'email': email,
            'contact_number': contact_number,
            'street': street,
            'pin_code': pin_code,
            'country': country,
            'created_at': datetime.utcnow(),
            'role': 'user'
        }
        result = self.collection.insert_one(user_data)

        if result.inserted_id:
            return {'message': 'user registered successfully', 'status': 'success'}, 200
        else:
            return {'message': 'user not registered', 'status': 'fail'}, 500

    def find_user(self, email):
        user_data = self.collection.find_one({'email': email})
        if user_data:
            user_data["_id"] = str(user_data.get('_id'))
            user_data.pop('created_at', None)
            return user_data
        else:
            return None

    def update_profile(self, email, updated_data):
        self.collection.update_one(
            {"email": email},
            {'$set': updated_data}
        )
        return {"status": 'Success', "message": 'User profile updated successfully...'}, 200

import cloudinary.uploader
import certifi
import ssl
import os

ssl_context = ssl.create_default_context(cafile=certifi.where())

cloudinary.config(
    cloud_name="dwipafwjg",
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET_KEY"),
    secure=True
)

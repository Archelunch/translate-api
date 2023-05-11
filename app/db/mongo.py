import os

import motor.motor_asyncio

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.words

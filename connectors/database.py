""" ./connectors/database.py """
from pymongo import MongoClient
from pymongo.collection import Cursor, DeleteResult, InsertOneResult, UpdateResult

from connectors import Configuration


class Database(MongoClient):
    def __init__(self, config: Configuration):
        super().__init__(config.database_url, config.database_port, connect=False)

    async def request_band(self, payload: dict) -> InsertOneResult:
        return self.admin.bands.insert_one(payload)

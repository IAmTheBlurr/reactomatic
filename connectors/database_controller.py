""" ./connectors/database.py """
from pymongo import MongoClient
from pymongo.collection import Cursor, DeleteResult, InsertOneResult, UpdateResult

from connectors import Configuration


class DatabaseController(object):
    def __init__(self, config: Configuration):
        super().__init__(config.database_url, config.database_port, connect=False)

    async def request_band(self, band_name: str) -> UpdateResult:
        return self.admin.bands.update_one({'name': band_name}, {'$inc': {'count': 1}}, upsert=True)

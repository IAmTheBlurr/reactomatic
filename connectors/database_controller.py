""" ./connectors/database_controller.py """
import logging
import os
import sys

from typing import List

from pymongo import MongoClient
from pymongo.collection import UpdateResult

from connectors import Configuration


class DatabaseController(object):
    def __init__(self, config: Configuration):
        self.client = MongoClient(config.database_uri)
        self.db = self.client['admin']

    async def request_band(self, band_name: str) -> UpdateResult:
        return self.admin.bands.update_one({'name': band_name}, {'$inc': {'count': 1}}, upsert=True)

    async def show_bands(self):
        return [band['name'] for band in self.db.bands.find({})]

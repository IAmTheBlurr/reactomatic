""" ./connectors/database_controller.py """
import logging
import os
import sys

from typing import List

import pymongo
from pymongo import MongoClient
from pymongo.collection import UpdateResult

from connectors import Configuration


class DatabaseController(object):
    def __init__(self, config: Configuration):
        self.client = MongoClient(config.database_uri)
        self.db = self.client['admin']

    async def request_band(self, band_name: str) -> UpdateResult:
        return self.db.bands.update_one({'name': band_name}, {'$inc': {'count': 1}}, upsert=True)

    async def show_bands(self):
        return [band['name'] for band in self.db.bands.find({})]

    async def get_top_bands(self):
        return [band for band in self.db.bands.find(limit=10, sort=[('count', pymongo.DESCENDING)])]

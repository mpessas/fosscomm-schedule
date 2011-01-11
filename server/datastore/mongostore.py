# -*- coding: utf-8 -*-

import pymongo

class MongoStore(object):

    def __init__(self):
        self._connnection = None
        self._db = None

    def connect(self, db="fosscomm", host='localhost', port=27017):
        self._connection = pymongo.Connection(host, port)
        self._db = self._connection[db]

    def disconnect(self):
        self._connection.disconnect()

    def _get_collection(self):
        return self._db.presentations

    def setup():
        """Setup indices"""
        pass                    # TODO

    def set(self, doc):
        col = self._get_collection()
        return col.insert(doc)

    def get_mongo_id(self, mid):
        col = self._get_collection()
        return col.find_one({"_id": mid})

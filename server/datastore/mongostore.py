# -*- coding: utf-8 -*-
"""Module for using MongoDB as datastore."""

import pymongo
import contextlib


class MongoStore(object):
    """Class to interface with MongoDB."""

    def __init__(self):
        self._connection = None
        self._db = None

    def connect(self, dbname="fosscomm", host='localhost', port=27017):
        """Connect to mongodb."""
        self._connection = pymongo.Connection(host, port)
        self._db = self._connection[dbname]

    def disconnect(self):
        """Disconnect from MongoDb.

        It must be run, when the connection is no longer needed.
        """
        self._connection.disconnect()

    @contextlib.contextmanager
    def open(self):
        """Context manager to connect/diconnect to MongoDB."""
        self.connect()
        yield
        self.disconnect()

    def _get_collection(self):
        """Return the desired collection of the database."""
        return self._db.presentations

    def setup(self):
        """Setup indices"""
        pass                    # TODO

    def put(self, doc):
        """Add a new object to Datastore.

        Argument must be a python dictionary.
        """
        col = self._get_collection()
        return col.insert(doc)

    def get_mongo_id(self, mid):
        """Get the object by the _id attribute used by MongoDb."""
        col = self._get_collection()
        return col.find_one({"_id": mid})

    def get(self, name, value):
        """Get one item only"""
        col = self._get_collection()
        return col.find_one({name: value})

    def get_all(self):
        """Get all items.

        Returns a generator.
        """
        col = self._get_collection()
        return (doc for doc in col.find())

    def filter(self, **kwargs):
        """Get items that satisfy the given criteria.

        Returns a generator.
        """
        col = self._get_collection()
        return (doc for doc in col.find(kwargs))

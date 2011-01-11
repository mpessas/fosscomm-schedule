# -*- coding: utf-8 -*-

import unittest
from mongostore import MongoStore

class ObjClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_doc(self):
        return dict(x=self.x, y=self.y)


class TestMongoStore(unittest.TestCase):

    def setUp(self):
        self.dbname = "test_fosscomm"
        self.store = MongoStore()
        self.store.connect(self.dbname)

    def tearDown(self):
        self.store._connection.drop_database(self.dbname)
        self.store.disconnect()

    def test_set(self):
        obj = ObjClass(1, 2)
        self.assertTrue(self.store.set(obj))

    def test_get(self):
        obj = ObjClass(1, 2)
        doc = obj.as_doc()
        mid = self.store.set(obj)
        res = self.store.get_mongo_id(mid)
        self.assertEquals(res['x'], doc['x'])
        self.assertEquals(res['y'], doc['y'])


if __name__ == '__main__':
    unittest.main()

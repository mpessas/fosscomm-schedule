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
        self.assertTrue(self.store.set(obj.as_doc()))

    def test_get_mongo_id(self):
        obj = ObjClass(1, 2)
        doc = obj.as_doc()
        mid = self.store.set(doc)
        res = self.store.get_mongo_id(mid)
        self.assertEquals(res['x'], doc['x'])
        self.assertEquals(res['y'], doc['y'])

    def test_get(self):
        obj = ObjClass(1, 2)
        doc = obj.as_doc()
        mid = self.store.set(doc)
        res = self.store.get('x', 1)
        self.assertEquals(res['_id'], mid)

    def test_get_all(self):
        obj1 = ObjClass(1, 2)
        obj2 = ObjClass(2, 4)
        mid1 = self.store.set(obj1.as_doc())
        mid2 = self.store.set(obj2.as_doc())
        self.assertEquals(len([x for x in self.store.get_all()]), 2)


if __name__ == '__main__':
    unittest.main()

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
        self.assertRaises(TypeError, self.store.set, 4)
        self.assertRaises(TypeError, self.store.set, [1, 2])

    def test_get_mongo_id(self):
        res = self.store.get_mongo_id("123")
        self.assertTrue(res is None)
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
        res = self.store.get('x', 4)
        self.assertTrue(res is None)

    def test_get_all(self):
        self.assertEquals(len([x for x in self.store.get_all()]), 0)
        obj1 = ObjClass(1, 2)
        obj2 = ObjClass(2, 4)
        mid1 = self.store.set(obj1.as_doc())
        mid2 = self.store.set(obj2.as_doc())
        self.assertEquals(len([x for x in self.store.get_all()]), 2)

    def test_filter(self):
        obj1 = ObjClass(1, 2)
        obj2 = ObjClass(2, 4)
        obj3 = ObjClass(2, 5)
        mid1 = self.store.set(obj1.as_doc())
        mid2 = self.store.set(obj2.as_doc())
        mid3 = self.store.set(obj3.as_doc())
        res = self.store.filter(x=2)
        self.assertEquals(len([x for x in res]), 2)
        for r in res:
            self.assertEquals(r['x'], 2)
        res = [x for x in self.store.filter(x=1)]
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['x'], 1)
        res = [x for x in self.store.filter(x=2, y=4)]
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['x'], 2)
        self.assertEquals(res[0]['y'], 4)
        res = [x for x in self.store.filter(x=2, y=6)]
        self.assertEquals(len(res), 0)


if __name__ == '__main__':
    unittest.main()

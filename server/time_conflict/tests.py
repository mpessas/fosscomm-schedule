#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from graph import EventNode
from graph import NotReadyError


class TestEventNode(unittest.TestCase):

    def setUp(self):
        self.node = EventNode(3)
        self.attrs = self.node._EventNode__attrs.iterkeys()

    def test_initializer(self):
        node = EventNode(3, title=u"title", summary=u"summary")
        self.assertEquals(node.title, u"title")
        self.assertEquals(node._id, 3)
        self.assertEquals(node.summary, u"summary")
        self.assertTrue(node.speaker is None)
        self.assertRaises(AttributeError, EventNode, 3, t=u"title")

    def test_ready(self):
        """Check that EventNode._is_ready returns True,
        iff all fields are set.
        """
        for attr in self.attrs:
            self.assertFalse(self.node._is_ready())
            setattr(self.node, attr, "val")
        self.assertTrue(self.node._is_ready())

    def test_wrong_attribute(self):
        with self.assertRaises(AttributeError):
            setattr(self.node.wrong_attr, False)

    def test_start_time(self):
        time = "10:30"
        self.node.time_start = time
        self.assertEquals(self.node.starts(), time)

    def test_start_time(self):
        time = "10:30"
        self.node.time_end = time
        self.assertEquals(self.node.ends(), time)

    def test_add_conflicts(self):
        e = EventNode(5)
        self.node.add_conflict_with_node(e)
        self.assertTrue(e.get_id() in self.node.conflicts_with)

    def test_save(self):
        self.assertRaises(NotReadyError, self.node.save)
        # for attr in self.attrs:
        #     setattr(self.node, attr, "val")
        # self.node.save()


if __name__ == '__main__':
    unittest.main()

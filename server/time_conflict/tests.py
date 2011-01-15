#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from graph import  Node, Event
from graph import NotReadyError


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.node = Node(Event(3))
        self.attrs = self.node._wraps._attrs.iterkeys()

    def test_initializer(self):
        node = Node(Event(3, title=u"title", summary=u"summary"))
        self.assertEquals(node.title, u"title")
        self.assertEquals(node._id, 3)
        self.assertEquals(node.summary, u"summary")
        self.assertTrue(node.speaker is None)
        self.assertRaises(AttributeError, Event, 3, t=u"title")

    def test_ready(self):
        """Check that Event._is_ready returns True,
        iff all fields are set.
        """
        for attr in self.attrs:
            self.assertFalse(self.node._is_ready())
            setattr(self.node._wraps, attr, "val")
        self.assertTrue(self.node._is_ready())

    def test_wrong_attribute(self):
        with self.assertRaises(AttributeError):
            setattr(self.node.wrong_attr, False)

    def test_start_time(self):
        time = "10:30"
        self.node._wraps.time_start = time
        self.assertEquals(self.node.starts(), time)

    def test_start_time(self):
        time = "10:30"
        self.node._wraps.time_end = time
        self.assertEquals(self.node.ends(), time)

    def test_add_conflicts(self):
        e = Node(Event(5))
        self.node.add_conflict_with_node(e)
        self.assertTrue(e.get_id() in self.node.conflicts_with)

    def test_save(self):
        self.assertRaises(NotReadyError, self.node.save)
        for attr in self.attrs:
            setattr(self.node._wraps, attr, "val")
        self.node.save()


if __name__ == '__main__':
    unittest.main()

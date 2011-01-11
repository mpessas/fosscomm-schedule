# -*- coding: utf-8 -*-

import unittest
from graph import EventNode
from graph import NotReadyError


class TestEventNode(unittest.TestCase):

    def setUp(self):
        self.node = EventNode(3)
        self.attrs = self.node._EventNode__attrs.iterkeys()

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

    def test_save(self):
        self.assertRaises(NotReadyError, self.node.save)
        # for attr in self.attrs:
        #     setattr(self.node, attr, "val")
        # self.node.save()


if __name__ == '__main__':
    unittest.main()

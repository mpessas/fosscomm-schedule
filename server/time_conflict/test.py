# -*- coding: utf-8 -*-

import unittest
from graph import EventNode


class TestEventNode(unittest.TestCase):

    def setUp(self):
        self.node = EventNode(3)
        self.attrs = self.node._EventNode__attrs.iterkeys()

    def test_completion(self):
        """Check that EventNode._is_complete returns True,
        iff all fields are set.
        """
        for attr in self.attrs:
            self.assertFalse(self.node._is_complete())
            setattr(self.node, attr, "val")
        self.assertTrue(self.node._is_complete())

    def test_wrong_attribute(self):
        with self.assertRaises(AttributeError):
            setattr(self.node.wrong_attr, False)


if __name__ == '__main__':
    unittest.main()

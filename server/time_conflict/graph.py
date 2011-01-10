# -*- coding: utf-8 -*-
"""A module to resolve time conflicts for events.

Time is divided in ticks. Each tick is represented by a TimeNode. An
event is represented by an EventNode. Each EventNode has the
corresponding TimeNodes as neighbours.
Two EventNodes conflict iff they share at least one TimeNode.
"""

class Node(object):
    """A node in the graph."""

    def __init__(self, num):
        """Initializer."""
        self.__id = num
        self.neighbours = set()

    def has_neighbour(self, node):
        """Check, if node is a neighbour of self.

        @param node the node to check for
        @returns True, if neighbour. Else, False
        """
        if node in self.neighbours:
            return True
        return False

    def add_neighbour(self, node):
        """Add a neighbour to this node's neighbours.

        @param node the node to add to neighbours
        """
        self.neighbours.update(node)

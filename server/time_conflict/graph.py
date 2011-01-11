# -*- coding: utf-8 -*-
"""A module to resolve time conflicts for events.

Time is divided in ticks. Each tick is represented by a TimeNode. An
event is represented by an EventNode. Each EventNode has the
corresponding TimeNodes as neighbours.
Two EventNodes conflict iff they share at least one TimeNode.
"""

import collections
from errors import NotReadyError

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


class TimeNode(Node):
    """A node for time ticks."""

    def __init__(self, num, tick):
        super(TimeNode, self).__init__(num)
        self.__tick = tick

    @property
    def tick(self):
        return self.__tick


class EventNode(Node):
    """A node for the events."""

    def __init__(self, num):
        super(EventNode, self).__init__(num)
        self.__attrs = {}
        for key in ('title', 'speaker', 'summary', 'filename',
                    'time_start', 'time_end', 'day', 'room', 'conflicts_with'):
            self.__attrs[key] = None
        self.__initialized = True

    def _is_ready(self):
        """Check whether all attributes of the isntance are set.

        @returns True if all attributes are set
                 False else
        """
        return all(self.__attrs.itervalues())

    def ready_required(f):
        def new_f(*args, **kwargs):
            if args[0]._is_ready():
                f(*args, **kwargs)
            else:
                raise NotReadyError
        new_f.__name__ = f.__name__
        new_f.__doc__ = f.__doc__
        return new_f
    
    def __getattr__(self, name):
        """Allow access to fields of the event.

        @return the field, if it exists
                None, else
        """
        if not name in self.__attrs.iterkeys():
            raise AttributeError(name)
        return self.__attrs[name]

    def __setattr__(self, name, value):
        if not '_EventNode__initialized' in self.__dict__:
            super(EventNode, self).__setattr__(name, value)
        elif not name in self.__attrs.iterkeys():
            raise AttributeError(name)
        else:
            self.__attrs[name] = value

    @ready_required
    def save(self):
        """Save instance to storage."""
        pass
        

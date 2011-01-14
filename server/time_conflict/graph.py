# -*- coding: utf-8 -*-
"""A module to resolve time conflicts for events.

Time is divided in ticks. Each tick is represented by a TimeNode. An
event is represented by an EventNode. Each EventNode has the
corresponding TimeNodes as neighbours.
Two EventNodes conflict iff they share at least one TimeNode.
"""

import datetime
import collections
from errors import NotReadyError
import datastore


INTERVAL = 30


class Node(object):
    """A node in the graph."""

    def __init__(self, num):
        """Initializer."""
        self._id = num
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

    def __unicode__(self):
        return unicode("<TimeNode %s>" % self._id)


class TimeNode(Node):
    """A node for time ticks."""

    def __init__(self, num):
        super(TimeNode, self).__init__(num)

    @property
    def tick(self):
        return self._id


class EventNode(Node):
    """A node for the events."""

    def __init__(self, num, **kwargs):
        super(EventNode, self).__init__(num)
        self.__attrs = {}
        self._optional_attrs = ('filename', 'conflicts_with', )
        for key in ('title', 'speaker', 'summary', 'filename',
                    'time_start', 'time_end', 'day', 'room',
                    'conflicts_with'):
            self.__attrs[key] = kwargs.get(key)
            try:
                del kwargs[key]
            except KeyError:
                pass
        if 'id' in kwargs:
            del kwargs['id']
        if kwargs:
            raise AttributeError(unicode(kwargs))
        self.__initialized = True

    def _is_ready(self):
        """Check whether all attributes of the isntance are set.

        @returns True if all attributes are set
                 False else
        """
        return all(val for (key, val) in self.__attrs.iteritems()
                   if key not in self._optional_attrs)

    def ready_required(f):
        """Decorator to assert ready-ness of the instance."""
        def new_f(*args, **kwargs):
            if args[0]._is_ready():  # args[0] is always self
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
        store = datastore.DataStore()
        store.connect()
        store.setup()
        store.put(self.as_doc())

    def starts(self):
        return getattr(self, 'time_start')


def create_graph(events):
    events.sort(key=EventNode.starts)
    time_nodes = create_time_tree(events[0].time_start, events[-1].time_end)


def create_time_tree(time_start, time_end):
    (hours, minutes) = time_start.split(':')
    start = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    (hours, minutes) = time_end.split(':')
    end = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    num_ticks = (end.seconds - start.seconds) / 60 / INTERVAL
    print num_ticks
    nodes = []
    for tick in xrange(num_ticks):
        nodes.append(TimeNode(tick))
    return nodes

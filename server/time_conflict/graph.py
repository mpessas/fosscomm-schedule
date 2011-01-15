# -*- coding: utf-8 -*-
"""A module to resolve time conflicts for events.

Time is divided in ticks. Each tick is represented by a TimeNode. An
event is represented by an EventNode. Each EventNode has the
corresponding TimeNodes as neighbours.
Two EventNodes conflict iff they share at least one TimeNode.
"""

import datetime
import collections
import logging
from errors import NotReadyError
import datastore


INTERVAL = 30
_log = logging.getLogger('')

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
        self.neighbours.add(node)

    def get_id(self):
        return self._id

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self._id)

    def __unicode__(self):
        return unicode("<%s %s>" % (self.__class__.__name__, self._id))


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
        """Return the time the event starts."""
        return getattr(self, 'time_start')

    def ends(self):
        """Return the time the event ends."""
        return getattr(self, 'time_end')

    def add_conflict_with_node(self, node):
        if getattr(self, 'conflicts_with') is None:
            setattr(self, 'conflicts_with', set())
        self.conflicts_with.add(node.get_id())


def str_to_timedelta(time):
    """Convert the given time string to a timedelta object.

    @param time a time in hh:mm format
    @returns the corresponding timedelta object
    """
    (hours, minutes) = time.split(':')
    return datetime.timedelta(hours=int(hours), minutes=int(minutes))


def timedelta_to_ticks(t):
    """Convert a timedelta object to ticks.

    @param diff the timedelta object
    @returns the number of ticks for this object
    """
    return t.seconds / 60 / INTERVAL


def create_graph(events):
    """Create the graph.

    The graph consists of EventNodes connected to TimeNodes based on
    when the corresponding events take place.
    """
    events.sort(key=EventNode.starts)
    base_str = events[0].time_start
    ticks = create_time_tree(base_str, events[-1].time_end)
    base = str_to_timedelta(base_str)
    for e in events:
        start = str_to_timedelta(e.starts())
        end = str_to_timedelta(e.ends())
        start_tick = timedelta_to_ticks(start - base)
        end_tick = timedelta_to_ticks(end - base)
        for tick in xrange(start_tick, end_tick):
            _log.debug("Node %s has neighbour node %s." % (e, ticks[tick]))            
            e.add_neighbour(ticks[tick])
            ticks[tick].add_neighbour(e)
    return events


def create_time_tree(time_start, time_end):
    """Create a graph of TimeNodes.

    This is actually a list of nodes sorted by the tick they correspond to."""
    (hours, minutes) = time_start.split(':')
    start = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    (hours, minutes) = time_end.split(':')
    end = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    num_ticks = (end.seconds - start.seconds) / 60 / INTERVAL
    _log.debug("Number of ticks: %s" % num_ticks)
    nodes = []
    for tick in xrange(num_ticks):
        nodes.append(TimeNode(tick))
    return nodes


def find_conflicts(graph):
    """Finds the conflicts between events.

    The ids of the conflicted nodes are saved in the 'conflicts_with'
    attribute.
    """
    for node in graph:
        for neighbour in node.neighbours:
            for n in neighbour.neighbours:
                if n is node:
                    continue
                _log.info("Nodes %s and %s are in conflict." % (node, n))
                node.add_conflict_with_node(n)
                n.add_conflict_with_node(node)

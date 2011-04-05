# -*- coding: utf-8 -*-

import redis
import json
import contextlib


class RedisStore(object):

    def __init__(self):
        self._r = None
        self._key = "fosscomm2011:sessions:all"

    def connect(self, db=0, host='localhost', port=6379):
        self._r = redis.Redis(
            host=host, port=port, db=db
        )

    def disconnect(self):
        pass

    @contextlib.contextmanager
    def open(self):
        self.connect()
        yield
        self.disconnect()

    def setup(self):
        """Setup indices"""
        pass                    # TODO

    def put(self, doc):
        """Add a new object to Datastore.

        Argument must be a python dictionary.
        """
        if not isinstance(doc, dict):
            raise TypeError
        return self._r.hset(self._key, doc["id_"], json.dumps(doc))

    def get_by_id(self, id_):
        """Get the object by the id_ attribute."""
        res = self._r.hget(self._key, id_)
        if res is None:
            return None
        return json.loads(res)

    def get(self, name, value):
        """Get one item only"""
        sessions = self._r.hgetall(self._key)
        for session in sessions.itervalues():
            doc = json.loads(session)
            if doc[name] == value:
                return doc
        return None

    def get_all(self):
        """Get all items.

        Returns a generator.
        """
        return self._r.hvals(self._key)

    def filter(self, **kwargs):
        """Get items that satisfy the given criteria.

        Returns a generator.
        """
        sessions = self._r.hgetall(self._key)
        import pdb; pdb.set_trace();
        for session in sessions.itervalues():
            doc = json.loads(session)
            found = True
            for key, val in kwargs.iteritems():
                if doc[key] != val:
                    found = False
            if found:
                yield doc

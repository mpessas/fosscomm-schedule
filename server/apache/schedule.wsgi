import os
os.chdir(os.path.dirname(__file__))

from bottle import Bottle, response, debug
app = Bottle()
debug(True)
import json

from datastore import DataStore


@app.get('/')
def get_events():
    """Return a list of all events."""
    ds = DataStore()
    with ds.open():
        res = ds.get_all()
    doc = []
    for r in res:
        del r['_id']            # Don't reveal these
        doc.append(r)
    response.set_content_type('application/json')
    return json.dumps(doc)


@app.get(':eid')
def get_event(eid):
    """Return the event with the specified id."""
    ds = DataStore()
    with ds.open():
        res = ds.get('id', int(eid))
    del res['_id']              # Don't reveal this
    return res

application = app

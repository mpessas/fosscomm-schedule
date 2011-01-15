import os
os.chdir(os.path.dirname(__file__))

from bottle import Bottle, static_file, response, debug
app = Bottle()
debug(True)
import json

from datastore import DataStore

@app.get('/')
def get_data():
    ds = DataStore()
    ds.connect()
    res = ds.get_all()
    ds.disconnect()
    doc = []
    for r in res:
        del r['_id']
        doc.append(r)
    response.set_content_type('application/json')
    return json.dumps(doc)

@app.get(':eid')
def get_event(eid):
    ds = DataStore()
    ds.connect()
    res = ds.get('id', int(eid))
    ds.disconnect()
    del res['_id']
    return res

application = app

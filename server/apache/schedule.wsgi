import os
os.chdir(os.path.dirname(__file__))

from bottle import Bottle, static_file, debug
app = Bottle()
debug(True)

@app.get(':filename')
def get_data(filename):
    return static_file(filename, root=".", mimetype="application/json")

application = app

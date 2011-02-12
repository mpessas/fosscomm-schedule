import os
os.chdir(os.path.dirname(__file__))

import datetime
import json
from bottle import Bottle, request, response, abort, debug, view
app = Bottle()
debug(True)
import icalendar

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

@app.get('/presentation/:pid#[0-9]+#')
@view('presentation.tpl')
def view_presentation(pid):
    ds = DataStore()
    with ds.open():
        res = ds.get('id', int(pid))
    return dict(speaker=res['speaker'],
                title=res['title'],
                summary=res['summary'],
                day = res['day'],
                start = res['time_start'],
                end=res['time_end'],
                room=res['room'],
    )

@app.get('/fosscomm.ical')
def get_ical():
    """Return an ical with the specified events."""
    events = request.GET.get('events', '')
    if events == '':
        abort(500, "No events specified")
    events = events.split(':')
    for i, event in enumerate(events):
        try:
            events[i] = int(event)
        except ValueError:
            abort(500, "Malformed query string provided")
    ds = DataStore()
    with ds.open():
        res = ds.filter(id={'$in': events})
    cal = icalendar.Calendar()
    cal.add('version', '2.0')
    for r in res:
        event = icalendar.Event()
        event['uid'] = "%s@patras.fosscomm.gr" % r['id']
        summary = "%s, %s" % (r['title'], r['speaker'])
        event.add('summary', summary)
        event.add('location', r['room'])
        event.add('dtstamp', datetime.datetime.utcnow())
        event.add('dtstart', event_time_to_datetime(r['day'], r['time_start']))
        event.add('dtend', event_time_to_datetime(r['day'], r['time_end']))
        event.add('description', r['summary'])
        cal.add_component(event)
    response.set_content_type('text/calendar')
    return cal.as_string()

def event_time_to_datetime(e_day, e_time):
    """Convert day/time of the event to an datetime object."""
    # Conference takes place on 7-8 May 2011
    if e_day == 1:
        day = 7
    else:
        day = 8
    (hours, minutes) = e_time.split(':')
    return datetime.datetime(2011, 5, day,
                             int(hours), int(minutes), 0,
                             tzinfo=icalendar.LocalTimezone())

application = app

import os
os.chdir(os.path.dirname(__file__))

import datetime
import json
from bottle import Bottle, request, response, abort, debug, view
app = Bottle()
debug(True)
import icalendar

from datastore import DataStore


def cmp_events(e1, e2):
    if e1['day'] < e2['day']:
        return -1
    elif e1['day'] > e2['day']:
        return 1
    e1_starts = e1['time_start'].split(':')
    e1_hour, e1_minute = int(e1_starts[0]), int(e1_starts[1])
    e2_starts = e2['time_start'].split(':')
    e2_hour, e2_minute = int(e2_starts[0]), int(e2_starts[1])
    if e1_hour < e2_hour:
        return -1
    elif e1_hour == e2_hour:
        if e1_minute < e2_minute:
            return -1
        elif e1_minute == e2_minute:
            return 0
        else:
            return 1
    else:
        return 1


@app.get('/')
def get_events():
    """Return a list of all events."""
    ds = DataStore()
    with ds.open():
        res = ds.get_all()
    doc = []
    for r in res:
        doc.append(json.loads(r))
    doc.sort(cmp_events)
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
        abort(400, "No events specified")
    events = events.split(':')
    for i, event in enumerate(events):
        try:
            events[i] = int(event)
        except ValueError:
            abort(400, "Malformed query string provided")
    ds = DataStore()
    with ds.open():
        res = ds.filter('id', events)
    cal = icalendar.Calendar()
    cal.add('version', '2.0')
    for r in res:
        print r['id']
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

@app.post('/register/')
def register():
    jid = request.POST.get("jid_input")
    if not jid:
        abort(400, "No JID provided")
    events = request.POST.get("events").split(':')
    if events == '':
        abort(400, "No events specified")
    for i, event in enumerate(events):
        try:
            events[i] = int(event)
        except ValueError:
            abort(400, "Malformed query string provided")
    ds = DataStore()
    with ds.open():
        for event in events:
            key = "fosscomm2011:session:%d" % event
            print key
            ds.add_to_set(key, jid)
    return json.dumps(True)

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

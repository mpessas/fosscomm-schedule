#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
import json
import graph


def parse_cmd_options(argv):
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Import FOSSCOMM events as json data."
    )
    parser.add_argument(
        'filename', help='file with the events in json format'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help=u'verbose output'
    )
    args = parser.parse_args(argv)
    return args


def get_events_from_file(filename):
    """Read the events from the specified file.

    Events must bein json format.
    """
    with open(filename) as f:
        events = json.load(f)
    event_node_list = []
    for e in events:
        event_node_list.append(graph.Node(graph.Event(e['id'], **e)))
    return event_node_list


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_cmd_options(argv)

    logger = logging.getLogger('')
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    filename = args.filename
    logger.debug("Filename: %s" % filename)
    eventlist = get_events_from_file(filename)
    logger.info("%s events found" % len(eventlist))
    max_day = max(e.day for e in eventlist)
    for day in xrange(1, max_day+1):
        events = graph.create_graph([e for e in eventlist if e.day == day])
        graph.find_conflicts(events)
        for e in events:
            print e.get_id(), e.conflicts_with

if __name__ == '__main__':
    sys.exit(main())

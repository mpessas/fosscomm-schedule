#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import graph

def parse_cmd_options(argv):
    parser = argparse.ArgumentParser(
        description="Import FOSSCOMM events as json data."
    )
    parser.add_argument(
        'filename', help='file with the events in json format'
    )
    args = parser.parse_args(argv)
    return args

def get_events_from_file(filename):
    with open(filename) as f:
        events = json.load(f)
    event_node_list = []
    for e in events:
        event_node_list.append(graph.EventNode(e['id'], **e))
    return event_node_list

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_cmd_options(argv)
    filename = args.filename
    eventlist = get_events_from_file(filename)
    graph.create_graph([e for e in eventlist if e.day==u"Σάββατο"])

if __name__ == '__main__':
    sys.exit(main())

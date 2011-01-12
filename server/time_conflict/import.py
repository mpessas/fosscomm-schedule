#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import json

def parse_cmd_options(argv):
    parser = argparse.ArgumentParser(
        description="Import FOSSCOMM events as json data."
    )
    parser.add_argument(
        'filename', help='file with the events in json format'
    )
    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_cmd_options(argv)
    filename = args.filename
    with open(filename) as f:
        events = json.load(f)
    event_node_list = []
    for e in events:
        event_node_list.append(EventNode(e['id']))
        event_node_list[-1].title = e['title']
        event_node_list[-1]

if __name__ == '__main__':
    sys.exit(main())

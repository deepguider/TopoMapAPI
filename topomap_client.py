from __future__ import print_function

import base64
import requests
import os
import geojson
import argparse
import sys


IP="localhost"
ROUTING_SERVER_URL = 'http://{}:21500/'.format(IP)
STREETVIEW_SERVER_URL = 'http://{}:21501/'.format(IP)
POI_SERVER_URL = 'http://{}:21502/'.format(IP)

def query_to_server(url, req):
    if req['type']=='tile':
        req_str = url + '{}/{}/{}'.format(req['type'], req['tile_num_x'], req['tile_num_y'])
    elif req['type']=='wgs':
        req_str = url + '{}/{}/{}/{}'.format(req['type'], req['latitude'], req['longitude'], req['radius'])
    elif req['type'] in ['node', 'routing_node']:
        req_str = url + '{}/{}/{}'.format(req['type'], req['node_id'], req['radius'])
    else:
        print('{} is not a valid request type'.format(req['type']))
        return None

    response = requests.get(req_str)
    response.raise_for_status()
    elapsed_time = response.elapsed.total_seconds()
    outputs = response.json()
    return outputs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Topological Map Client")
    parser.add_argument("server_type", type=str, help="request type (routing, streetview, or poi)")
    parser.add_argument("req_type", type=str, help="request type (tile, wgs, or node)")
    args = parser.parse_args()

    if args.server_type=="routing":
        SERVER_URL = ROUTING_SERVER_URL
    elif args.server_type=="streetview":
        SERVER_URL = STREETVIEW_SERVER_URL
    elif args.server_type=="poi":
        SERVER_URL = POI_SERVER_URL
    else:
        print("Not suppported server type")
        sys.exit()

    if args.req_type=="tile":
        req = {'type': 'tile', 'tile_num_x': 55897, 'tile_num_y': 25393}
    elif args.req_type=="wgs":
        req = {'type': 'wgs', 'latitude': 37.513366, 'longitude': 127.056132, 'radius': 500.0}
        #req = {'type': 'wgs', 'latitude': 30, 'longitude': 120} # Invalid request (out of range)
    elif args.req_type=="node":
        if args.server_type=="routing":
            req = {'type': 'node', 'node_id': 559512564700400, 'radius': 500.0} # For routing layers
        elif args.server_type=="streetview":
            req = {'type': 'node', 'node_id': 33004500884, 'radius': 200.0} # For streetview layers
        elif args.server_type=="poi":
            req = {'type': 'node', 'node_id': 929272521, 'radius': 300.0} # For Poi layers
    elif args.req_type=="rnode":
        req = {'type': 'routing_node', 'node_id': 559512564700400, 'radius': 500.0}
    else:
        print("Not suppported request type")
        sys.exit()

    res = query_to_server(SERVER_URL, req)
    if res != None:
        with open("{}_{}.geojson".format(args.server_type, args.req_type),'w') as f:
            geojson.dump(res, f)

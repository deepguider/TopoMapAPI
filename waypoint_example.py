from __future__ import print_function

import base64
import requests
import os
import json
import argparse
import sys
import numpy as np
import geojson
import time

IP="localhost"
SERVER_URL = 'http://{}:20005/'.format(IP)

def query_to_server(url, req):
    req_str = url + '{}/{}/{}/{}/{}'.format(req['start_lat'], req['start_lon'], req['goal_lat'], req['goal_lon'], req['num_paths'])
    response = requests.get(req_str)
    response.raise_for_status()
    elapsed_time = response.elapsed.total_seconds()
    outputs = response.json()
    return outputs

def modify_edge(url, req):
    req_str = url + '{}/{}'.format(req['cmd'],req['edge_num'])
    response = requests.get(req_str)
    response.raise_for_status()
    elapsed_time = response.elapsed.total_seconds()
    outputs = response.json()
    return outputs

def merge_routes(routes):
    route_all = []
    ids = []
    for rt in routes:
        this_route = rt['features']
        if len(route_all)==0:
            route_all.extend(this_route)
            ids.extend([x['properties']['id'] for x in this_route])
        else:
            for r in this_route:
                _id = r['properties']['id']
                if _id not in ids:
                    route_all.append(r)
                    ids.append(_id)
    merged_route = geojson.FeatureCollection(route_all)
    return merged_route

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Topological Map Client")
    args = parser.parse_args()

    ##Example 2: Start -> Waypoint -> Goal
    start = (127.37464, 36.38559)
    waypoint = (127.37696, 36.38560)
    goal = (127.37845, 36.38553)
    reqs = [{'start_lon': start[0], 'start_lat': start[1], 'goal_lon': waypoint[0], 'goal_lat': waypoint[1], 'num_paths':1},
            {'start_lon': waypoint[0], 'start_lat': waypoint[1], 'goal_lon': goal[0], 'goal_lat': goal[1], 'num_paths':1}]

    routes = []
    for i, req in enumerate(reqs):
        res = query_to_server(SERVER_URL, req)
        routes.append(res[0])
        time.sleep(0.1)

    merged = merge_routes(routes)
    with open("results/test2_route.geojson",'w') as f:
        json.dump(merged, f)


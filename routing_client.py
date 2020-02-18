from __future__ import print_function

import base64
import requests
import os
import json
import argparse
import sys
import numpy as np
import geojson


IP="localhost"
SERVER_URL = 'http://{}:20005/'.format(IP)

def query_to_server(url, req):
    req_str = url + '{}/{}/{}/{}/{}'.format(req['start_lat'], req['start_lon'], req['goal_lat'], req['goal_lon'], req['num_paths'])
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

    ##Example 1: Start -> Goal
    req = {'start_lon': 127.367541, 'start_lat': 36.383912, 'goal_lon': 127.378538, 'goal_lat': 36.379558, 'num_paths':2} # ETRI
    #req = {'start_lon': 127.047569, 'start_lat': 37.503884, 'goal_lon': 127.0621, 'goal_lat': 37.5087, 'num_paths':2} # COEX
    res = query_to_server(SERVER_URL, req)
    for i, r in enumerate(res): 
        with open("route_{}.geojson".format(i),'w') as f:
            json.dump(r, f)

    '''
    ##Example 2: Start -> Waypoint -> Goal
    start = (127.367541, 36.383912)
    waypoint = (127.378407, 36.385565)
    goal = (127.378538, 36.379558)
    reqs = [{'start_lon': start[0], 'start_lat': start[1], 'goal_lon': waypoint[0], 'goal_lat': waypoint[1], 'num_paths':1},
            {'start_lon': waypoint[0], 'start_lat': waypoint[1], 'goal_lon': goal[0], 'goal_lat': goal[1], 'num_paths':1}]

    routes = []
    for i, req in enumerate(reqs):
        res = query_to_server(SERVER_URL, req)
        routes.append(res[0])
        with open("route_{}.geojson".format(i),'w') as f:
            json.dump(res[0], f)

    merged = merge_routes(routes)
    with open("route.geojson",'w') as f:
        json.dump(merged, f)
    '''



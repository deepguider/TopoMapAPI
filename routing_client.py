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

    ## Example 1: Start -> Goal
    reqs = [{'start_lon': 127.367433, 'start_lat': 36.382423, 'goal_lon': 127.378857, 'goal_lat': 36.379444, 'num_paths':1}] # ETRI
    reqs += [{'start_lon': 127.367541, 'start_lat': 36.383912, 'goal_lon': 127.378538, 'goal_lat': 36.379558, 'num_paths':1}]
    reqs += [{'start_lon': 127.375976, 'start_lat': 36.385862, 'goal_lon': 127.373817, 'goal_lat': 36.385399, 'num_paths':1}]
    reqs += [{'start_lon': 127.047569, 'start_lat': 37.503884, 'goal_lon': 127.0621, 'goal_lat': 37.5087, 'num_paths':1}] # COEX
    reqs += [{'start_lon': 127.060953, 'start_lat': 37.511474, 'goal_lon': 127.0621623, 'goal_lat': 37.506841, 'num_paths':1}]
    reqs += [{'start_lon': 127.060953, 'start_lat': 37.511474, 'goal_lon': 127.052455, 'goal_lat': 37.509813, 'num_paths':1}]
    reqs += [{'start_lon': 127.043224, 'start_lat': 37.503015, 'goal_lon': 127.060953, 'goal_lat': 37.511474, 'num_paths':1}]
    reqs += [{'start_lon': 126.76248647136512, 'start_lat': 37.50827147263543, 'goal_lon': 126.77883995105907, 'goal_lat': 37.5202294735007, 'num_paths':1}] # Bucheon #1
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'goal_lon': 126.77883995105907, 'goal_lat': 37.5202294735007, 'num_paths':1}] # Bucheon #2
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'goal_lon': 126.76248647136512, 'goal_lat': 37.50827147263543, 'num_paths':1}] # Bucheon #3
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'goal_lon': 126.76322666164481, 'goal_lat': 37.505081040743846, 'num_paths':1}] # Bucheon #4
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'goal_lon': 126.7764346349311, 'goal_lat': 37.503434908041186, 'num_paths':1}] # Bucheon #5
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'goal_lon': 126.77141266168167, 'goal_lat': 37.523458632728094,  'num_paths':1}] # Bucheon #6

    for i, req in enumerate(reqs):
        res = query_to_server(SERVER_URL, req)
        time.sleep(0.1)
        for k, r in enumerate(res):
            with open("results/test1_query{}_route{}.geojson".format(i, k),'w') as f:
                json.dump(r, f)

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
        time.sleep(0.1)

    merged = merge_routes(routes)
    with open("results/test2_route.geojson",'w') as f:
        json.dump(merged, f)
    """
    ## Example 3: Delete edge => Restore edge
    # Original route
    req = {'start_lon': 127.367433, 'start_lat': 36.382423, 'goal_lon': 127.378857, 'goal_lat': 36.379444, 'num_paths':2} # ETRI
    res = query_to_server(SERVER_URL, req)
    with open("results/test3_route_before.geojson",'w') as f:
            json.dump(res[0], f)

    # Delete edge
    req = {'cmd': 'delete', 'edge_num': 559542564810231}
    res = modify_edge(SERVER_URL, req)
    print(res)

    req = {'start_lon': 127.367433, 'start_lat': 36.382423, 'goal_lon': 127.378857, 'goal_lat': 36.379444, 'num_paths':2} # ETRI
    res = query_to_server(SERVER_URL, req)
    with open("results/test3_route_edge_removed.geojson",'w') as f:
            json.dump(res[0], f)

    # Restore edge
    req = {'cmd': 'restore', 'edge_num': 559542564810231}
    res = modify_edge(SERVER_URL, req)
    print(res)

    req = {'start_lon': 127.367433, 'start_lat': 36.382423, 'goal_lon': 127.378857, 'goal_lat': 36.379444, 'num_paths':2} # ETRI
    res = query_to_server(SERVER_URL, req)
    with open("results/test3_route_edge_restored.geojson",'w') as f:
            json.dump(res[0], f)
    """
    

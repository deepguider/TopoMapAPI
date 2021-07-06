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
    req_str = url + '{}/{}/{}/{}/{}/{}/{}'.format(req['start_lat'], req['start_lon'], req['start_floor'], req['goal_lat'], req['goal_lon'], req['goal_floor'], req['num_paths'])
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
    reqs = [{'start_lon': 127.368066, 'start_lat': 36.380074, 'start_floor': 7,  'goal_lon': 127.367587, 'goal_lat': 36.380064, 'goal_floor': 7, 'num_paths':1}] # ETRI 7th floor
    reqs += [{'start_lon': 127.367963, 'start_lat': 36.380153, 'start_floor': 7,  'goal_lon': 127.367512, 'goal_lat': 36.380095, 'goal_floor': 3, 'num_paths':1}] # ETRI 7th floor to 3rd floor
    reqs += [{'start_lon': 127.367596, 'start_lat': 36.379929, 'start_floor': 1,  'goal_lon': 127.3677889, 'goal_lat': 36.380323, 'goal_floor': 7, 'num_paths':1}] # ETRI 1st floor to 7th floor
    reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.368314, 'goal_lat': 36.383912, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside
    reqs += [{'start_lon': 127.365641, 'start_lat': 36.379706, 'start_floor': 0,  'goal_lon': 127.367449, 'goal_lat': 36.380058, 'goal_floor': 7, 'num_paths':1}] # ETRI outside -> 1st floor -> 7th floor
    reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.373393, 'goal_lat': 36.385344, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside
    #reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.377734, 'goal_lat': 36.385511, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside
    reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.378449, 'goal_lat': 36.385287, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside
    reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.378821, 'goal_lat': 36.387919, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside
    reqs += [{'start_lon': 127.367818, 'start_lat': 36.38014, 'start_floor': 7,  'goal_lon': 127.364792, 'goal_lat': 36.382382, 'goal_floor': 0, 'num_paths':1}] # ETRI 7th floor -> 3rd floor -> outside

    """
    reqs += [{'start_lon': 127.047569, 'start_lat': 37.503884, 'start_floor': 0, 'goal_lon': 127.0621, 'goal_lat': 37.5087, 'goal_floor': 0, 'num_paths':1}] # COEX
    reqs += [{'start_lon': 127.060953, 'start_lat': 37.511474, 'start_floor': 0, 'goal_lon': 127.0621623, 'goal_lat': 37.506841, 'goal_floor': 0, 'num_paths':1}]
    reqs += [{'start_lon': 127.060953, 'start_lat': 37.511474, 'start_floor': 0, 'goal_lon': 127.052455, 'goal_lat': 37.509813, 'goal_floor': 0, 'num_paths':1}]
    reqs += [{'start_lon': 127.043224, 'start_lat': 37.503015, 'start_floor': 0, 'goal_lon': 127.060953, 'goal_lat': 37.511474, 'goal_floor': 0, 'num_paths':1}]
    reqs += [{'start_lon': 126.76248647136512, 'start_lat': 37.50827147263543, 'start_floor': 0, 'goal_lon': 126.77883995105907, 'goal_lat': 37.5202294735007, 'goal_floor': 0, 'num_paths':1}] # Bucheon #1
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'start_floor': 0, 'goal_lon': 126.77883995105907, 'goal_lat': 37.5202294735007, 'goal_floor': 0, 'num_paths':1}] # Bucheon #2
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'start_floor': 0, 'goal_lon': 126.76248647136512, 'goal_lat': 37.50827147263543,'goal_floor': 0,  'num_paths':1}] # Bucheon #3
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'start_floor': 0, 'goal_lon': 126.76322666164481, 'goal_lat': 37.505081040743846, 'goal_floor': 0, 'num_paths':1}] # Bucheon #4
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'start_floor': 0, 'goal_lon': 126.7764346349311, 'goal_lat': 37.503434908041186, 'goal_floor': 0, 'num_paths':1}] # Bucheon #5
    reqs += [{'start_lon': 126.7638630710112, 'start_lat': 37.516289426170985, 'start_floor': 0, 'goal_lon': 126.77141266168167, 'goal_lat': 37.523458632728094, 'goal_floor': 0, 'num_paths':1}] # Bucheon #6
    """
    for i, req in enumerate(reqs):
        res = query_to_server(SERVER_URL, req)
        time.sleep(0.1)
        for k, r in enumerate(res):
            with open("results/test1_query{}_route{}.geojson".format(i, k),'w') as f:
                json.dump(r, f)
    """
    ##Example 2: Start -> Waypoint -> Goal
    start = (127.37464, 36.38559)
    waypoint = (127.37696, 36.38560)
    goal = (127.37845, 36.38553)
    reqs = [{'start_lon': start[0], 'start_lat': start[1], 'start_floor': 0, 'goal_lon': waypoint[0], 'goal_lat': waypoint[1], 'goal_floor': 0, 'num_paths':1},
            {'start_lon': waypoint[0], 'start_lat': waypoint[1],'start_floor': 0, 'goal_lon': goal[0], 'goal_lat': goal[1], 'goal_floor': 0, 'num_paths':1}]

    routes = []
    for i, req in enumerate(reqs):
        res = query_to_server(SERVER_URL, req)
        routes.append(res[0])
        time.sleep(0.1)

    merged = merge_routes(routes)
    with open("results/test2_route.geojson",'w') as f:
        json.dump(merged, f)
    """
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

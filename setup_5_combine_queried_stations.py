'''
Final step of the station query.

Combines the final results of the TFL and OSM station queries.

Reads from OSM_FILTERED, TFL_FILTERED.
Writes to COMBINED_STATIONS.
'''

import json

from constants.dataset_paths import COMBINED_STATIONS, TFL_FILTERED, OSM_FILTERED

with open(OSM_FILTERED, 'r', encoding='utf8') as osm_f:
    osm_queried_stations = json.load(osm_f)
    with open(TFL_FILTERED, 'r', encoding='utf8') as tfl_f:
        tfl_queried_stations = json.load(tfl_f)

        combined_lookup = {}

        for osm_station_name, osm_station_value in osm_queried_stations.items():
            if osm_station_value:
                if osm_station_name not in combined_lookup:
                    combined_lookup[osm_station_name] = {
                        'tflType': '',
                        'id': '',
                        'url': '',
                        'commonName': '',
                        'placeType': '',
                        'additionalProperties': [],
                        'children': [],
                        'childrenUrls': [],
                        'lat': 51.486343,
                        'lon': -0.122492,
                    }
                combined_lookup[osm_station_name]['placeId'] = osm_station_value[
                    'place_id'
                ]
                combined_lookup[osm_station_name]['licence'] = osm_station_value[
                    'licence'
                ]
                combined_lookup[osm_station_name]['osmType'] = osm_station_value[
                    'osm_type'
                ]
                combined_lookup[osm_station_name]['osmId'] = osm_station_value['osm_id']
                combined_lookup[osm_station_name]['lat'] = float(
                    osm_station_value['lat']
                )
                combined_lookup[osm_station_name]['lon'] = float(
                    osm_station_value['lon']
                )
                combined_lookup[osm_station_name]['class'] = osm_station_value['class']
                combined_lookup[osm_station_name]['osmWayType'] = osm_station_value[
                    'type'
                ]
                combined_lookup[osm_station_name]['placeRank'] = osm_station_value[
                    'place_rank'
                ]
                combined_lookup[osm_station_name]['importance'] = osm_station_value[
                    'importance'
                ]
                combined_lookup[osm_station_name]['addressType'] = osm_station_value[
                    'addresstype'
                ]
                combined_lookup[osm_station_name]['name'] = osm_station_value['name']
                combined_lookup[osm_station_name]['displayName'] = osm_station_value[
                    'display_name'
                ]
                combined_lookup[osm_station_name]['boundingBox'] = osm_station_value[
                    'boundingbox'
                ]

        for tfl_station_name, tfl_station_value in tfl_queried_stations.items():
            if tfl_station_value:
                if tfl_station_name not in combined_lookup:
                    combined_lookup[tfl_station_name] = {
                        'placeId': 0,
                        'licence': '',
                        'osmType': '',
                        'osmId': 0,
                        'lat': '',
                        'lon': '',
                        'class': '',
                        'osmWayType': '',
                        'placeRank': 0,
                        'importance': 0,
                        'addressType': '',
                        'name': tfl_station_value['commonName'],
                        'displayName': tfl_station_value['commonName'],
                        'boundingBox': [],
                    }
                combined_lookup[tfl_station_name]['tflType'] = tfl_station_value[
                    '$type'
                ]
                combined_lookup[tfl_station_name]['id'] = tfl_station_value['id']
                combined_lookup[tfl_station_name]['url'] = tfl_station_value['url']
                combined_lookup[tfl_station_name]['commonName'] = tfl_station_value[
                    'commonName'
                ]
                combined_lookup[tfl_station_name]['placeType'] = tfl_station_value[
                    'placeType'
                ]
                combined_lookup[tfl_station_name]['additionalProperties'] = (
                    tfl_station_value['additionalProperties']
                )
                combined_lookup[tfl_station_name]['children'] = tfl_station_value[
                    'children'
                ]
                combined_lookup[tfl_station_name]['childrenUrls'] = tfl_station_value[
                    'childrenUrls'
                ]
                combined_lookup[tfl_station_name]['lat'] = tfl_station_value['lat']
                combined_lookup[tfl_station_name]['lon'] = tfl_station_value['lon']

            result = []

            for _, station in combined_lookup.items():
                result.append(station)

            with open(COMBINED_STATIONS, 'w', encoding='utf8') as out_f:
                out_f.write(json.dumps(result))

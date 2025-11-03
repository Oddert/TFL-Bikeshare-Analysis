"""
Intakes the result of the OSM full query and attempts to reduce the list of results to a single choice.

Depends on the output from `attempt_requery_empty_station.py`.
"""

import json
import re
import requests

from time import sleep
from typing import List

with open("./osm-supplied-stations.json", "r", encoding="utf8") as f:
    print(f)
    requeried_stations = json.load(f)
    print(requeried_stations)

    number_requeried = len(requeried_stations)
    filtered_response = {}

    def select_from_multiple_choice(station_name: str, choices: List[dict]):
        """Prompts users to select from one or more choices from the OSM API."""
        print("   ")
        print(
            f'Item {idx}/{number_requeried} "{station_name}", has multiple results. Please choose from this list: '
        )
        print("   ")

        for i, location in enumerate(choices):
            print(f"{i} ========================================================")
            print('class: ', location['class'])
            print('type: ', location['type'])
            print('addresstype: ', location['addresstype'])
            print('name: ', location['name'])
            print('osm_type: ', location['osm_type'])

        valid_input = False
        while not valid_input:
            user_input = input("Item index (indicated above the choices): ")
            # validate input
            if not re.match("[0-9]+", user_input):
                print(
                    f'"{user_input}" is not a valid index choice, please enter an index.'
                )
            elif int(user_input) + 1 >= len(choices) or int(user_input) < 0:
                print(
                    '"{user_input}" is not a valid index choice, please enter an index.'
                )
            else:
                valid_input = True

        filtered_response[station_name] = choices[
            int(user_input)
        ]

    for idx, station in enumerate(requeried_stations):
        item = requeried_stations[station]
        print("        ")
        print("--------")
        print("        ")
        if len(item) == 0:
            print(f'Item {idx}/{number_requeried} "{station}" has no entries.')

            query_loop = True
            while query_loop:
                choose_additional_query = input(
                    "Would you like to try another search term (y/N)?"
                )
                choose_additional_query_strp = choose_additional_query.lower().strip()
                if choose_additional_query_strp == "y" or choose_additional_query_strp == 'yes':
                    user_query = input("Search term: ")
                    print(f'Attempting OpenStreetMap query for "{user_query}"...')
                    try:
                        sleep(1)
                        url = f"https://nominatim.openstreetmap.org/search?q={user_query}&format=json&countrycodes=gb"
                        response = requests.get(
                            url, timeout=3000, headers={"User-Agent": "robyn veitch"}
                        )
                        print(response)
                        response_json = response.json()
    
                        if len(response_json) == 1:
                            print("...one result provided: ")
                            user_choice_use_result = input("Use this result (Y/n)? ")
                            if user_choice_use_result:
                                filtered_response[station] = response_json
                                query_loop = False
                        elif len(response_json) == 0:
                            print("...no results returned.")
                            filtered_response[station] = None
                        else:
                            select_from_multiple_choice(station, response_json)
                            query_loop = False

                    except Exception as ex:
                        print(ex)
                elif choose_additional_query_strp == 'n' or choose_additional_query_strp == 'no':
                    print(f'User declined to re-enter. Setting "{station}" to null.')
                    query_loop = False
                    filtered_response[station] = None
                else:
                    print('Please enter yes or no.')
        elif len(item) == 1:
            print(f"Item {idx}/{number_requeried} has only 1 entry, writing that one.")
            filtered_response[station] = requeried_stations[station][0]
        else:
            select_from_multiple_choice(station, item)

    print(filtered_response)

    filtered_response_json_str = json.dumps(filtered_response)

    with open("osm-supplied-stations-selected.json", "w", encoding="utf8") as f:
        f.write(filtered_response_json_str)

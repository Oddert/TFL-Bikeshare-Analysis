"""
Loads the queried station data from the TFL API and resolves down to one station per station name.

Reads from TFL_STATIONS.
Writes to TFL_FILTERED.
"""

import json
import re

from constants.dataset_paths import TFL_FILTERED, TFL_STATIONS

with open(TFL_STATIONS, encoding='utf8') as f:
    stations_queried = json.load(f)

    stations_queried_filtered = {}

    for name, value in stations_queried.items():
        if not value:
            stations_queried_filtered[name] = None
        elif len(value) == 1:
            stations_queried_filtered[name] = value[0]
        else:
            print(f'Multiple results found for "{name}", please choose from: ')
            for idx, station in enumerate(value):
                print(f'   {idx}. {station["commonName"]}')

            valid_input = False
            while not valid_input:
                user_input = input('Item index (indicated above the choices): ')
                # validate input
                if not re.match('[0-9]+', user_input):
                    print(
                        f'"{user_input}" is not a valid index choice, please enter an index.'
                    )
                elif int(user_input) + 1 > len(value):
                    print(
                        '"{user_input}" is out of range (too high), please enter a valid index.'
                    )
                elif int(user_input) < 0:
                    print(
                        '"{user_input}" is out of range (too low), please enter a valid index.'
                    )
                else:
                    valid_input = True

            stations_queried_filtered[name] = value[int(user_input)]  # type: ignore

    filtered_json_str = json.dumps(stations_queried_filtered)

    with open(TFL_FILTERED, 'w', encoding='utf8') as f:
        f.write(filtered_json_str)

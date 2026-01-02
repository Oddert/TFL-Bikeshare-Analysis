'''Holds application level constant variables denoting where specific files are output to / read from.'''

# Top-level folder containing the computed datasets.
CALCULATED_DATASET_FOLDER = 'computed_data'

# File to hold the result of the TFL API query.
TFL_STATIONS = f'{CALCULATED_DATASET_FOLDER}/tfl-supplied-stations.json'

# File to hold the result of the TFL API query.
TFL_FILTERED = f'{CALCULATED_DATASET_FOLDER}/tfl-supplied-stations-selected.json'

# File to hold the result of the OSM API query.
OSM_STATIONS = f'{CALCULATED_DATASET_FOLDER}/osm-supplied-stations.json'

# File to hold the result of re-queried data from the OSM query.
OSM_FILTERED = f'{CALCULATED_DATASET_FOLDER}/osm-supplied-stations-selected.json'

# File with the combined station data from all sources.
COMBINED_STATIONS = f'{CALCULATED_DATASET_FOLDER}/combined-stations.json'

# File with the combined station data in list / array format.
COMBINED_STATIONS_LIST = f'{CALCULATED_DATASET_FOLDER}/combined-stations-list.json'

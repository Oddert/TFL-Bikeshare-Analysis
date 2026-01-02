"""
Performs a station query against the OSM API for one station name.

Appends the result to the existing query file if it exists, otherwise writes to that file as a single entry.

Will either use a hard-coded station or, if a second argument is provided, will use that value instead.

Writes to the path OSM_STATIONS.
"""

import json
import requests
import sys

from loguru import logger

from constants.dataset_paths import OSM_STATIONS

station = 'Strand, Strand_OLD'

if len(sys.argv) > 1:
    logger.info(f'Received command line arguments: {sys.argv}')
    if len(sys.argv) > 2:
        logger.warning(
            'Multiple arguments were passed in, only the first will be used for the query. This could indicate a delineator in your station name, for example a comma. Please check and consider adding quotation marks to ensure thw whole name is used.'
        )
    station = sys.argv[1]

url = f'https://nominatim.openstreetmap.org/search?q={station}&format=json&countrycodes=gb'
logger.info(f'Querying: {url}')

try:
    with open(OSM_STATIONS, encoding='utf8') as f:
        stations_queried = json.load(f)
        logger.info('Existing station list found, appending...')
except FileNotFoundError:
    stations_queried = {}
    logger.info('No existing list found, will write a single result...')

response = requests.get(url, timeout=3000, headers={'User-Agent': 'robyn veitch'})
response_json = response.json()
stations_queried[station] = response_json

logger.info('Result: ')
logger.info(response_json)

json_str = json.dumps(stations_queried)

with open(OSM_STATIONS, 'w', encoding='utf8') as f:
    f.write(json_str)
    logger.info(f'Written to {OSM_STATIONS}')

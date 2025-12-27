# London Bike Share August 2023 Analysis

## File Structure & Naming Pattern

Files prefixed with `playground_` or `example_` are working files used to try ideas or contain modified exampels from the internet.

Files prefixed with `setup_` relate to the main data query, cleaning, and post-processing steps taken, split out in order to selectively repeat steps.

## Processing & Data Cleaning Steps

1. setup_1_query_unique_stations.py
    - Reads Kaggle DS
    - Writes to `TFL_STATIONS`
2. setup_2_attempt_requery_empty_station.py
    - Reads `TFL_STATIONS`
    - Write to `OSM_STATIONS`
3. setup_3_filter_osm_results.py
    - Reads `OSM_STATIONS`
    - Writes to `OSM_STATIONS_FILTERED`
4. TODO setup_4_combine_queried_stations.py
    - ???

## Data Example & Column Names

Number|Start date|Start station number|Start station|End date|End station number|End station|Bike number|Bike model|Total duration|Total duration (ms)
---|---|---|---|---|---|---|---|---|---|---
132825189|8/1/2023 0:00|1190|"Kennington Lane Rail Bridge, Vauxhall"|8/1/2023 0:17|1059|"Albert Embankment, Vauxhall"|23715|CLASSIC|16m 46s|1006663
132825190|8/1/2023 0:00|1190|"Kennington Lane Rail Bridge, Vauxhall"|8/1/2023 0:17|1059|"Albert Embankment, Vauxhall"|41267|CLASSIC|16m 47s|1007128
132825191|8/1/2023 0:00|983|"Euston Road, Euston"|8/1/2023 0:11|3500|"Baldwin Street, St. Luke's"|53180|CLASSIC|11m 6s|666395
132825192|8/1/2023 0:01|3479|"Old Brompton Road, South Kensington"|8/1/2023 0:12|1140|"Grosvenor Road, Pimlico"|53431|CLASSIC|11m 53s|713059

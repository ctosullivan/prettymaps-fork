from geopandas import GeoDataFrame
from shapely.geometry import Point

from prettymapsfork import fetch

# Test data

# Example gdf data
gdf_data = {
    'Name': ['Location A', 'Location B', 'Location C'],
    'Value': [10, 20, 30]
}
# Coordinates for the points
gdf_coordinates = [
    Point(-73.935242, 40.730610),  # New York
    Point(-118.243683, 34.052235),  # Los Angeles
    Point(-87.623177, 41.881832)   # Chicago
]
# Create the GeoDataFrame
test_gdf = GeoDataFrame(gdf_data, geometry=gdf_coordinates)

test_coordinates = gdf_coordinates[0]

test_tuple = -73.935242, 40.730610

# test OSMid - string
test_osmid  = "175905"  # New York

test_address = """Wall Street, William Street, Whitehall, Financial District, Manhattan, New York County, New York, 10005, United States"""

def test_parse_query():
    parser = fetch.QueryParser()

    # test GeoDataFrame
    assert parser.parse_query(test_gdf) == "polygon"

    # test coordinates - Point
    assert parser.parse_query(test_coordinates) == "coordinates"

    # test coordinates - Tuple
    assert parser.parse_query(test_tuple) == "coordinates"

    assert parser.parse_query(test_osmid) == "osmid"

    #test address - string
    assert parser.parse_query(test_address) == "address"

def test_get_boundary():
    parser = fetch.QueryParser()

    # test coordinates - Point
    assert isinstance(parser.get_boundary(test_coordinates, radius=10), GeoDataFrame) == True

    # test coordinates - Tuple
    assert isinstance(parser.get_boundary(test_tuple, radius=10), GeoDataFrame) == True

    assert isinstance(parser.get_boundary(test_osmid, radius=10), GeoDataFrame) == True

    #test address - string
    assert isinstance(parser.get_boundary(test_address, radius=10), GeoDataFrame) == True
    



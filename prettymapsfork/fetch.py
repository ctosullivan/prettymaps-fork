"""
Prettymaps/Prettymapsfork - A minimal Python library to draw pretty maps from OpenStreetMap Data
Copyright (C) 2021 Marcelo Prates
Copyright (C) 2024 Cormac O' Sullivan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re
from typing import Tuple

import osmnx as ox
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import (
    Point,
    Polygon,
)
from shapely.ops import transform
from shapely.affinity import rotate

class QueryParser:

    def parse_query(
            self, 
            query: str | Tuple | GeoDataFrame | Point
        ) -> str | None:
        """Function to parse input query and classify based on query type.
        Args:
            query: GeoDataFrame | str | Tuple- input query to be classified
        Returns:
            str: string classifying the input query as follows:
                GeoDataFrame-                   "polygon"
                Tuple / Point-                  "coordinates"
                Text in range [0-9](digits)-    "osmid"
                Other text inputs-              "address"
        """
        if isinstance(query, GeoDataFrame):
            return "polygon"
        elif isinstance(query, tuple) or isinstance(query, Point):
            return "coordinates"
        elif re.match(r"[0-9]+", query):
            return "osmid"
        elif re.match(r"\S+", query):
            return "address"
        else:
            print("Please enter valid location details.")
            return None
        
    def get_boundary(
            self,
            query: str | Tuple | GeoDataFrame | Point,
            radius: int,
            is_circular: bool=False,
            rotation: int=0,
        ) -> GeoDataFrame:
        """ Function to get a square or circular boundary around a point. 
        Args:
            query: GeoDataFrame | str | Tuple- input query
            radius: int- radius of boundary (square or circular)
            is_circular: bool- indicates if boundary is circular
            rotation: int- degree of rotation for boundary
        """
        # Get point from query
        parser = QueryParser()
        if parser.parse_query(query) == "coordinates":
            point = query
        else:
            point = ox.geocode(query)

        # Create GeoDataFrame from point
        # Flip the points in the query
        if isinstance(point, Point):
            transform(lambda x, y: (y, x), point)
        elif isinstance(point, Tuple):
            point = Point(point[::-1])

        boundary = ox.projection.project_gdf(
            GeoDataFrame(geometry=[point], crs="EPSG:4326")
        )

        if is_circular:
            # use .buffer() to expand point into circle
            boundary.geometry = boundary.geometry.buffer(radius)
        else: 
            # Square shape
            x, y = np.concatenate(boundary.geometry[0].xy)
            r = radius
            boundary = GeoDataFrame(
                geometry=[
                    rotate(
                        Polygon(
                            [(x - r, y - r), 
                             (x + r, y - r), 
                             (x + r, y + r), 
                             (x - r, y + r)]
                        ),
                        rotation,
                    )
                ],
                crs=boundary.crs,
            )

        # Unproject
        boundary = boundary.to_crs(4326)

        return boundary
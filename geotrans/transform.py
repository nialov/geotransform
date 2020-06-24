"""
File: transform.py
Author: nialov
Email: nikolasovaskainen@gmail.com
Github: https://github.com/nialov
Description: Main module in charge of all transformations.
"""

import geopandas as gpd
import fiona
from pathlib import Path
from typing import List, Tuple

GEOPACKAGE = "gpkg"
SHAPEFILE = "shp"
FILEGEODATABASE = "gdb"


def load_file(filestr: str) -> list:
    """
    Takes a single geodata filepath string, determines its type and returns a 
    list of GeoDataFrames and a list of layer
    names that consist of all file data.
    """
    filepath = Path(filestr)
    # Throw errors if filepath is invalid
    check_file(filepath)
    # Determine geodata type
    filetype = determine_filetype(filepath)
    if filetype == GEOPACKAGE:
        # Can contain multiple layers.
        geodataframes, layers = load_geopackage(filepath)


def check_file(filepath: Path) -> None:
    """
    Checks that filepath is valid and file is valid but not if its a geodata
    file.
    """
    # Check that file exists
    if not filepath.exists():
        raise FileNotFoundError(f"File was not found. Filepath: {filepath}")
    # Test if path is a directory
    if filepath.is_dir():
        # Test if directory was a filegeodatabase
        if f".{FILEGEODATABASE}" not in str(filepath):
            raise IsADirectoryError(f"Filepath was a directory: {filepath}")
    return


def determine_filetype(filepath: Path) -> str:
    """
    Takes a single geodata filepath and determines its geodata type.
    """
    if GEOPACKAGE in str(filepath.suffix):
        return GEOPACKAGE
    elif SHAPEFILE in str(filepath.suffix):
        return SHAPEFILE
    elif FILEGEODATABASE in str(filepath.suffix):
        return FILEGEODATABASE
    else:
        raise TypeError(
            "Filepath was not recognized or was not an implemented type. \n"
            f"Filepath: {filepath}"
        )
    return


def load_geopackage(filepath: Path) -> Tuple[List[gpd.GeoDataFrame], List[str]]:
    """
    Use fiona to parse geopackage layers. Returns a list of GeoDataFrames 
    and a list layer names.
    """
    geodataframes = []
    layer_names = []
    # TODO: Better implementation, replace try-except with proper method.
    for i in range(1000):
        # Tries to read layer names using a running index. When this fails
        # -> break the for loop.
        try:
            name = fiona.open(filepath, layer=i).name
            geodataframe = gpd.read_file(filepath, layer=i)
            geodataframes.append(geodataframe)
            layer_names.append(name)
        except:
            break
    return geodataframes, layer_names


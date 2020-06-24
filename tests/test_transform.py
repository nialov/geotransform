"""
File: test_transform.py
Author: nialov
Email: nikolasovaskainen@gmail.com
Github: https://github.com/nialov
Description: pytests for transform.py
"""
from geotrans import transform

from pathlib import Path
import geopandas as gpd

test_file_path = Path("tests/data/OG1_tulkinta_filtered_5m.gpkg")
test_dir_path = Path("tests/data")
test_invalid_path = Path("tests/datarrr")


def test_check_file():
    assert transform.check_file(test_file_path) is None
    try:
        transform.check_file(test_dir_path)
    except IsADirectoryError:
        pass
    try:
        transform.check_file(test_invalid_path)
    except FileNotFoundError:
        pass


def test_determine_filetype():
    assert transform.determine_filetype(test_file_path) == transform.GEOPACKAGE


def test_load_geopackage():
    geodataframes, layer_names = transform.load_geopackage(test_file_path)

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)

    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)

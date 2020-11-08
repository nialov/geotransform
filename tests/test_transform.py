"""
Description: pytests for transform.py
"""
from geotrans import transform
from geotrans.transform import (
    GEOPACKAGE_DRIVER,
    SHAPEFILE_DRIVER,
    FILEGEODATABASE_DRIVER,
)
from pathlib import Path
import geopandas as gpd
import fiona
from tests import Helpers
import pytest


def test_check_file():
    assert transform.check_file(Helpers.test_multilayer_file_path) is None
    try:
        transform.check_file(Helpers.test_dir_path)
    except IsADirectoryError:
        pass
    try:
        transform.check_file(Helpers.test_invalid_path)
    except FileNotFoundError:
        pass


@pytest.mark.parametrize(
    "file_path,assumed_filetype", Helpers.test_determine_filetype_params
)
def test_determine_filetype(file_path: Path, assumed_filetype: str):
    assert transform.determine_filetype(file_path) == assumed_filetype


@pytest.mark.parametrize("file_path", Helpers.test_load_multilayer_params)
def test_load_multilayer(file_path: Path):
    geodataframes, layer_names = transform.load_multilayer(
        Helpers.test_multilayer_file_path
    )

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)
    assert len(geodataframes) != 0
    assert len(geodataframes) == len(layer_names)

    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)


def test_load_singlelayer():
    geodataframes, layer_names = transform.load_singlelayer(
        Helpers.test_singlelayer_file_path,
        transform.determine_filetype(Helpers.test_singlelayer_file_path),
    )

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)

    assert len(geodataframes) + len(layer_names) == 2
    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)


def test_load_geojson():
    geodataframes, layer_names = transform.load_singlelayer(
        Helpers.test_geojson_file_save_path,
        transform.determine_filetype(Helpers.test_geojson_file_save_path),
    )

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)

    assert len(geodataframes) + len(layer_names) == 2
    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)


def test_single_save_file_geojson(tmp_path):
    # tmp_path is a temporary Path directory
    geodataframes, layer_names = transform.load_singlelayer(
        Helpers.test_singlelayer_file_path,
        transform.determine_filetype(Helpers.test_singlelayer_file_path),
    )
    filenames = [tmp_path / Helpers.test_single_file_save_path_geojson]
    try:
        transform.save_files(
            geodataframes,
            layer_names,
            transform_to_type=transform.GEOJSON,
            filenames=filenames,
        )
    except fiona.errors.SchemaError:
        print([gdf.columns for gdf in geodataframes])
        raise


def test_single_save_file(tmp_path):
    # tmp_path is a temporary Path directory
    geodataframes, layer_names = transform.load_singlelayer(
        Helpers.test_singlelayer_file_path,
        transform.determine_filetype(Helpers.test_singlelayer_file_path),
    )
    filenames = [tmp_path / Helpers.test_single_file_save_path]
    try:
        transform.save_files(
            geodataframes,
            layer_names,
            filenames=filenames,
            transform_to_type=transform.SHAPEFILE,
        )
    except fiona.errors.SchemaError:
        print([gdf.columns for gdf in geodataframes])
        raise


def test_multi_layer_save(tmp_path):
    geodataframes, layer_names = transform.load_multilayer(
        Helpers.test_multilayer_file_path
    )
    assert len(geodataframes) == len(layer_names) == 2
    filenames = []
    for layer_name in layer_names:
        filenames.append(tmp_path / f"{layer_name}_test_multi_layer.shp")
    transform.save_files(geodataframes, layer_names, filenames, transform.SHAPEFILE)


def test_driver_strings():
    for driver in [GEOPACKAGE_DRIVER, SHAPEFILE_DRIVER, FILEGEODATABASE_DRIVER]:
        assert driver in fiona.supported_drivers


def test_load_filegeodatabase(tmp_path):
    """
    Helpers.tests loading a filegeodatabase.
    """
    geodataframes, layer_names = transform.load_multilayer(
        Helpers.test_filegeodatabase_file_path
    )
    assert len(geodataframes) == len(layer_names)
    filenames = []
    for layer_name in layer_names:
        filenames.append(tmp_path / f"{layer_name}_test_filegeodatabase.shp")
    # Save to multiple shapefiles
    transform.save_files(geodataframes, layer_names, filenames, transform.SHAPEFILE)
    # Save same files to a single geopackage
    filenames = [tmp_path / f"saving_filegeodatabase.gpkg"]
    transform.save_files(geodataframes, layer_names, filenames, transform.GEOPACKAGE)

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

test_multilayer_file_path = Path("tests/data/Two_Layer_Geopackage_OG6_OG7.gpkg")
test_singlelayer_file_path = Path("tests/data/branches_cropped_Domain_IIId.shp")
test_dir_path = Path("tests/data")
test_invalid_path = Path("tests/datarrr")

test_filegeodatabase_file_path = Path("tests/data/OG1_faults.gdb")

test_single_file_save_path = Path("i_hope_this_is_saved.gpkg")


def test_check_file():
    assert transform.check_file(test_multilayer_file_path) is None
    try:
        transform.check_file(test_dir_path)
    except IsADirectoryError:
        pass
    try:
        transform.check_file(test_invalid_path)
    except FileNotFoundError:
        pass


def test_determine_filetype():
    assert (
        transform.determine_filetype(test_multilayer_file_path) == transform.GEOPACKAGE
    )


def test_load_multilayer():
    geodataframes, layer_names = transform.load_multilayer(test_multilayer_file_path)

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)

    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)


def test_load_singlelayer():
    geodataframes, layer_names = transform.load_singlelayer(test_singlelayer_file_path)

    assert isinstance(geodataframes, list)
    assert isinstance(layer_names, list)

    assert len(geodataframes) + len(layer_names) == 2
    for gdf, name in zip(geodataframes, layer_names):
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert isinstance(name, str)


def test_single_save_file(tmp_path):
    # tmp_path is a temporary Path directory
    geodataframes, layer_names = transform.load_singlelayer(test_singlelayer_file_path)
    filenames = [tmp_path / test_single_file_save_path]
    try:
        transform.save_files(
            geodataframes,
            layer_names,
            savefile_driver=transform.GEOPACKAGE_DRIVER,
            filenames=filenames,
        )
    except fiona.errors.SchemaError:
        print([gdf.columns for gdf in geodataframes])
        raise


def test_multi_layer_save(tmp_path):
    geodataframes, layer_names = transform.load_multilayer(test_multilayer_file_path)
    assert len(geodataframes) == len(layer_names) == 2
    filenames = []
    for layer_name in layer_names:
        filenames.append(tmp_path / f"{layer_name}_test_multi_layer.shp")
    transform.save_files(
        geodataframes, layer_names, filenames, savefile_driver=SHAPEFILE_DRIVER
    )


def test_driver_strings():
    for driver in [GEOPACKAGE_DRIVER, SHAPEFILE_DRIVER, FILEGEODATABASE_DRIVER]:
        assert driver in fiona.supported_drivers


def test_load_filegeodatabase(tmp_path):
    """
    Tests loading a filegeodatabase.
    """
    geodataframes, layer_names = transform.load_multilayer(
        test_filegeodatabase_file_path
    )
    assert len(geodataframes) == len(layer_names)
    filenames = []
    for layer_name in layer_names:
        filenames.append(tmp_path / f"{layer_name}_test_filegeodatabase.shp")
    # Save to multiple shapefiles
    transform.save_files(
        geodataframes, layer_names, filenames, savefile_driver=SHAPEFILE_DRIVER
    )
    # Save same files to a single geopackage
    filenames = [tmp_path / f"saving_filegeodatabase.gpkg"]
    transform.save_files(
        geodataframes, layer_names, filenames, savefile_driver=GEOPACKAGE_DRIVER
    )

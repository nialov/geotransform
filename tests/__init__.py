from pathlib import Path
import geotrans.transform as transform
import pytest


class Helpers:

    test_multilayer_file_path = Path("tests/data/Two_Layer_Geopackage_OG6_OG7.gpkg")
    test_singlelayer_file_path = Path("tests/data/branches_cropped_Domain_IIId.shp")
    test_dir_path = Path("tests/data")
    test_invalid_path = Path("tests/datarrr")

    test_filegeodatabase_file_path = Path("tests/data/OG1_faults.gdb")
    test_geojson_file_save_path = Path("tests/data/Hastholmen_LiDAR_lineaments.geojson")

    test_single_file_save_path = Path("i_hope_this_is_saved.gpkg")
    test_single_file_save_path_geojson = Path("i_hope_this_is_saved.geojson")

    test_determine_filetype_params = [
        (test_multilayer_file_path, transform.GEOPACKAGE),
        (test_singlelayer_file_path, transform.SHAPEFILE),
        (test_filegeodatabase_file_path, transform.FILEGEODATABASE),
        (test_geojson_file_save_path, transform.GEOJSON),
        pytest.param(test_dir_path, transform.FILEGEODATABASE, marks=pytest.mark.xfail),
    ]

    test_load_multilayer_params = [
        (test_multilayer_file_path),
        (test_filegeodatabase_file_path),
        (test_singlelayer_file_path),
    ]

"""
Description: Module in charge of all loading and saving.
"""

from pathlib import Path
from typing import List, Tuple

import fiona
import geopandas as gpd
import click

GEOPACKAGE = "gpkg"
SHAPEFILE = "shp"
FILEGEODATABASE = "gdb"
GEOJSON = "geojson"

GEOPACKAGE_DRIVER = "GPKG"
SHAPEFILE_DRIVER = "ESRI Shapefile"
FILEGEODATABASE_DRIVER = "OpenFileGDB"
GEOJSON_DRIVER = "GeoJSON"

driver_dict = {
    GEOPACKAGE: GEOPACKAGE_DRIVER,
    SHAPEFILE: SHAPEFILE_DRIVER,
    FILEGEODATABASE: FILEGEODATABASE_DRIVER,
    GEOJSON: GEOJSON_DRIVER,
}
MULTILAYER_CAPABLE = [GEOPACKAGE, FILEGEODATABASE]
SAVE_CAPABLE = [GEOPACKAGE, SHAPEFILE, GEOJSON]
FILETYPES = [GEOPACKAGE, SHAPEFILE, FILEGEODATABASE, GEOJSON]
SUPPORTS_LAYER_NAMES = [GEOPACKAGE, SHAPEFILE, FILEGEODATABASE]


def load_file(filepath: Path) -> Tuple[List[gpd.GeoDataFrame], List[str]]:
    """
    Takes a single geodata filepath string, determines its type and returns a
    list of GeoDataFrames and a list of layer
    names that consist of all file data.
    """
    # Throw errors if filepath is invalid
    check_file(filepath)
    # Determine geodata type
    filetype = determine_filetype(filepath)
    if filetype in MULTILAYER_CAPABLE:
        # Can contain multiple layers.
        geodataframes, layer_names = load_multilayer(filepath)
    elif filetype in FILETYPES:
        # Only containts a single layer
        geodataframes, layer_names = load_singlelayer(filepath, filetype)
        assert len(geodataframes) + len(layer_names) == 2
    else:
        # TODO: More supported types
        raise NotImplementedError(
            "Only geopackages, filegeodatabases, geojsons"
            "and shapefiles are currently supported"
        )
    return geodataframes, layer_names


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
    for filetype in FILETYPES:
        if filetype in str(filepath.suffix):
            return filetype
    raise TypeError(
        "Filepath was not recognized or was not an implemented type. \n"
        f"Filepath: {filepath}"
    )


def load_multilayer(filepath: Path) -> Tuple[List[gpd.GeoDataFrame], List[str]]:
    """
    Use fiona to parse geopackage and filegeodatabase layers.
    Returns a list of GeoDataFrames and a list layer names.

    Will also work on single layer files.
    """
    geodataframes = []
    layer_names = []
    for i in range(len(fiona.listlayers(filepath))):
        # fiona.listlayers lists all layer names
        with fiona.open(filepath, layer=i) as opened:
            name = opened.name
            geodataframe = gpd.read_file(filepath, layer=i)
            geodataframes.append(geodataframe)
            layer_names.append(name)
    return geodataframes, layer_names


def load_singlelayer(
    filepath: Path, filetype: str
) -> Tuple[List[gpd.GeoDataFrame], List[str]]:
    """
    Load a single layer from a geodata file.
    """
    geodataframes = []
    layer_names = []
    geodataframes.append(gpd.read_file(filepath))
    # TODO: Opening twice, inefficient.
    if filetype in SUPPORTS_LAYER_NAMES:
        try:
            layer_names.append(fiona.open(filepath).name)
        except ValueError:
            click.echo(
                f"Filetype {filetype} errored out when trying to get" "layer name."
            )
            raise
    else:
        layer_names.append(filepath.name)

    return geodataframes, layer_names


def save_files(
    geodataframes: List[gpd.GeoDataFrame],
    layer_names: List[str],
    filenames: List[Path],
    transform_to_type: str,
) -> None:
    """
    The user can save his geodata files with multiple different options.

    If a directory is given, the geodata files are saved to that directory
    with the acquired layer names.
    If a single filename is given all geodata is saved to that file and this
    option requires checking that the format can handle multiple layers i.e.
    if shapefile is the save option: it cannot handle multiple layers and
    an error is thrown.

    Filenames is a list of Paths that have been checked to be valid.
    If user inputted no filenames: the filename will be made from layer name
    before this function.
    """
    assert len(geodataframes) != 0
    assert len(layer_names) != 0
    assert len(filenames) != 0
    savefile_driver = driver_dict[transform_to_type]
    if savefile_driver == GEOPACKAGE_DRIVER:
        geodataframes = validate_loaded_geodataframes(geodataframes, layer_names)

    if len(geodataframes) > 1 and len(filenames) == 1:
        # Multiple layers to single file.
        # Make sure geodatatype can handle multiple layers.
        # Make sure layer names are unique
        assert savefile_driver in [GEOPACKAGE_DRIVER]
        assert len(set(layer_names)) == len(layer_names)
        for geodataframe, layer_name in zip(geodataframes, layer_names):
            geodataframe.to_file(filenames[0], layer=layer_name, driver=savefile_driver)
    else:
        # Save layers to files.
        for geodataframe, layer_name, filename in zip(
            geodataframes, layer_names, filenames
        ):
            if transform_to_type in SUPPORTS_LAYER_NAMES:
                geodataframe.to_file(filename, layer=layer_name, driver=savefile_driver)
            else:
                geodataframe.to_file(filename, driver=savefile_driver)


def validate_loaded_geodataframes(geodataframes, layer_names):
    """
    Some columns (namely FID) cause issues when saving to geopackage.
    Currently these columns are removed to remove the issue.
    """
    for geodataframe, layer_name in zip(geodataframes, layer_names):
        fid = "fid"
        if fid in geodataframe.columns:
            geodataframe.drop(columns=fid, inplace=True)
            click.echo(
                click.style(
                    f"Columns of layer: {layer_name} had to be modified.\n"
                    f"Field with name: {fid} was removed.",
                    fg="red",
                )
            )
    return geodataframes

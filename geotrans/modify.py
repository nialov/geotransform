"""
Description: WORK IN PROGRESS. NO INTEGRATION.
             Modifies geopandas layers with scripts
"""

import geopandas as gpd
import click


def check_for_nan(layer: gpd.GeoDataFrame) -> None:
    """
    Check for nan in layer columns and prints the number of nan in each column.
    """
    layer_columns = layer.columns
    assert len(layer_columns) > 0
    for column in layer_columns:
        nan_in_column = layer["column"].isnull().sum()
        to_print = f"{column} has {nan_in_column} null values."
        click.echo(to_print)


def check_and_fix_invalid_geometries(
    layer: gpd.GeoDataFrame, fix: bool
) -> gpd.GeoDataFrame:
    """
    Check for invalid geometries in layer and fix them (if able)
    when fix == True.
    """
    # Check for nan in geometry column
    nan_in_geometry = layer.geometry.isna()


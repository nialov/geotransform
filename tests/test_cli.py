"""
Description: pytests for cli.py
"""

from pathlib import Path

import geopandas as gpd
import pytest
from click.testing import CliRunner, Result

from geotrans import cli, transform
from tests import Helpers


def test_validate_inputs():
    """
    Test validate_inputs.
    """
    cli.validate_inputs(Helpers.test_inputs, transform.GEOPACKAGE, Helpers.test_output)
    try:
        cli.validate_inputs("hello", "pretty sure", "this will fail")  # type: ignore
    except ValueError:
        pass


@pytest.mark.parametrize("inputs,transform_to_type", Helpers.test_run_transform_params)
def test_run_transform(inputs, transform_to_type, tmp_path: Path):
    """
    Test run_transform.
    """
    cli.run_transform(inputs, transform_to_type, str(tmp_path))
    for x in tmp_path.iterdir():
        if len(inputs) == 1:
            test_gdf = gpd.read_file(Path(x))
            original_gdf = gpd.read_file(inputs[0])
            # Test that all column strings match in original geodataframe and
            # the newly made geodataframe
            assert all(
                col1 == col2
                for col1, col2 in zip(test_gdf.columns, original_gdf.columns)
            )
            assert test_gdf.iloc[0, 0] == original_gdf.iloc[0, 0]


def test_run_transform_geojson(tmp_path):
    """
    Test run_transform_geojson.
    """
    cli.run_transform(Helpers.test_input_geojson, transform.GEOPACKAGE, tmp_path)
    for x in tmp_path.iterdir():
        assert Path(x).exists()
        test_gdf = gpd.read_file(Path(x))
        original_gdf = gpd.read_file(Path(Helpers.test_input_geojson[0]))
        # Test that all column strings match in original geodataframe and
        # the newly made geodataframe
        assert all(
            col1 == col2 for col1, col2 in zip(test_gdf.columns, original_gdf.columns)
        )
        assert test_gdf.iloc[0, 0] == original_gdf.iloc[0, 0]
        # Remove test files
        Path(x).unlink()
    cli.run_transform(Helpers.test_inputs, transform.GEOJSON, tmp_path)
    for x in tmp_path.iterdir():
        assert Path(x).exists()
        test_gdf = gpd.read_file(Path(x))
        original_gdf = gpd.read_file(Path(Helpers.test_inputs[0]))
        # Test that all column strings match in original geodataframe and
        # the newly made geodataframe
        assert all(
            col1 == col2 for col1, col2 in zip(test_gdf.columns, original_gdf.columns)
        )
        assert test_gdf.iloc[0, 0] == original_gdf.iloc[0, 0]
        # Remove test files
        Path(x).unlink()


def test_command_line_integration(tmp_path):
    """
    Tests click functionality.
    """
    clirunner = CliRunner()
    output_file = "cli_test"
    cli_args = [
        "tests/data/KL5_tulkinta.shp",
        "--to_type",
        "gpkg",
        "--output",
        f"{tmp_path}/{output_file}",
    ]
    result = clirunner.invoke(cli.main, cli_args)
    # Check that exit code is 0 (i.e. ran succesfully.)
    assert result.exit_code == 0
    # Checks if output path is printed
    assert str(tmp_path) in result.output
    assert (Path(tmp_path) / Path(f"{output_file}.gpkg")).exists()


def test_command_line_integration_gpkg_to_shp(tmp_path):
    """
    Tests click functionality.
    """
    clirunner = CliRunner()
    output_file = "cli_test"
    cli_args = [
        "tests/data/OG1_tulkinta_filtered_5m.gpkg",
        "--to_type",
        "shp",
        "--output",
        f"{tmp_path}/{output_file}",
    ]
    result = clirunner.invoke(cli.main, cli_args)
    # Check that exit code is 0 (i.e. ran succesfully.)
    assert result.exit_code == 0
    # Checks if output path is printed
    assert str(tmp_path) in result.output
    assert (Path(tmp_path) / Path(f"{output_file}.shp")).exists()


def test_command_line_integration_gpkg_to_dir(tmp_path):
    """
    Tests click functionality.
    """
    assert len(list(Path(tmp_path).glob("*"))) == 0
    clirunner = CliRunner()
    cli_args = [
        "tests/data/OG1_tulkinta_filtered_5m.gpkg",
        "--to_type",
        "shp",
        "--output",
        f"{tmp_path}",
    ]
    result = clirunner.invoke(cli.main, cli_args)
    # Check that exit code is 0 (i.e. ran succesfully.)
    assert result.exit_code == 0
    # Checks if output path is printed
    assert str(tmp_path) in result.output
    # tmp_path_head = Path(tmp_path).name
    assert len(list(Path(tmp_path).glob("*"))) != 0


def test_cli_multilayer_to_folder(tmp_path: Path):
    """
    Test cli_multilayer_to_folder.
    """
    clirunner = CliRunner()
    cli_args = [
        str(Helpers.test_multilayer_file_path),
        "--to_type",
        "shp",
        "--output",
        f"{tmp_path}",
    ]
    result: Result = clirunner.invoke(cli.main, cli_args)
    # Check that exit code is 0 (i.e. ran succesfully.)
    if result.exit_code != 0:
        print(result.output)
    assert result.exit_code == 0
    # Checks if output path is printed
    assert str(tmp_path) in result.output
    # tmp_path_head = Path(tmp_path).name
    output_files = list(tmp_path.iterdir())
    assert len(list(Path(tmp_path).glob("*"))) != 0
    assert "OG6" in str(output_files)
    assert "OG7" in str(output_files)

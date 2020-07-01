"""
File: test_cli.py
Author: nialov
Email: nikolasovaskainen@gmail.com
Github: https://github.com/nialov
Description: pytests for cli.py
"""

from pathlib import Path
import pytest
import geopandas as gpd
from click.testing import CliRunner
from geotrans import cli
from geotrans import transform

test_inputs = ("tests/data/OG1_tulkinta_filtered_5m.gpkg",)
test_inputs2 = (
    "tests/data/OG1_tulkinta_filtered_5m.gpkg",
    "tests/data/OG4_fractures_ML_filtered_5m.gpkg",
)
test_transform_to_type = transform.GEOPACKAGE
test_output = "test.gpkg"


def test_validate_inputs():
    cli.validate_inputs(test_inputs, test_transform_to_type, test_output)
    try:
        cli.validate_inputs("hello", "pretty sure", "this will fail")
    except ValueError:
        pass


# def test_main(tmp_path):
#     runner = CliRunner()
#     result = runner.invoke(
#         cli.main, [[test_inputs][0], test_transform_to_type, str(tmp_path)]
#     )
# assert result.exit_code == 0
def test_run_transform(tmp_path: Path):
    if len(test_inputs) > 1:
        raise Exception(
            "Only one input accepted into this test. test_inputs "
            "needs to be a list of size 1."
        )
    cli.run_transform(test_inputs, test_transform_to_type, tmp_path)
    for x in tmp_path.iterdir():
        assert Path(x).exists()
        test_gdf = gpd.read_file(Path(x))
        original_gdf = gpd.read_file(Path(test_inputs[0]))
        # Test that all column strings match in original geodataframe and
        # the newly made geodataframe
        assert all(
            [col1 == col2 for col1, col2 in zip(test_gdf.columns, original_gdf.columns)]
        )
        assert test_gdf.iloc[0, 0] == original_gdf.iloc[0, 0]
        # Remove test files
        Path(x).unlink()
    # Run test with two input files
    cli.run_transform(test_inputs2, test_transform_to_type, tmp_path)
    # Test that two files exist because the output is a directory.
    assert sum([1 for _ in tmp_path.iterdir()]) == 2

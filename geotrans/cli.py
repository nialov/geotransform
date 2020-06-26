"""
File: cli.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description: Command line integration of geotransfrom.
"""
from typing import Iterable

import click
from pathlib import Path

import geotrans.transform as transform
from geotrans.transform import SHAPEFILE, GEOPACKAGE, FILEGEODATABASE, driver_dict


@click.command()
@click.argument(
    "inputs", type=click.Path(exists=True, readable=True, resolve_path=True), nargs=-1,
)
@click.option("transform_to_type", "--to_type", type=str, default=GEOPACKAGE)
@click.option(
    "output", "--output", type=click.Path(writable=True, file_okay=True, dir_okay=True)
)
def main(inputs, transform_to_type, output):
    """
    A variable amount of input filenames are accepted, the type to transfrom the input to 
    can be given and an output file or output directory can be given.
    If the output is a file: all layers are saved to that file if the given transform_to_type 
    supports multiple layers.
    If the output is a directory all input layers are saved to that directory based
    on their layer name.
    """
    validate_inputs(inputs, transform_to_type, output=None)
    run_transform(inputs, transform_to_type, output)


def run_transform(inputs, transform_to_type, output):
    """
    Runs functions in transform.py
    """
    geodataframes, layer_names = [], []
    for input_filename in inputs:
        gdfs, lnms = transform.load_file(Path(input_filename))
        geodataframes.extend(gdfs)
        layer_names.extend(lnms)
    if transform_to_type in [GEOPACKAGE, SHAPEFILE] and Path(output).exists():
        # Save individual geopackages or shapefiles to a given directory.
        save_paths = []
        for layer_name in layer_names:
            save_paths.append(Path(output) / Path(f"{layer_name}.{transform_to_type}"))

        transform.save_files(
            geodataframes,
            layer_names,
            save_paths,
            savefile_driver=driver_dict[transform_to_type],
        )
        finished(output)
    elif transform_to_type in [GEOPACKAGE] and not Path(output).is_dir():
        # Save a single geopackage output file with multiple layers
        # (if there are multiple layers in inputs).
        # Make sure file suffix is in the saved file.
        output = (
            output
            if f".{transform_to_type}" in output
            else f"{output}.{transform_to_type}"
        )
        transform.save_files(
            geodataframes,
            layer_names,
            [Path(output)],
            savefile_driver=driver_dict[transform_to_type],
        )
        finished(output)
    else:
        raise NotImplementedError(
            "Command line inputs did not match."
            "Implemented functionality.\n"
            f"{inputs, transform_to_type, output}"
        )


def validate_inputs(inputs, transform_to_type: str, output: str) -> None:
    if transform_to_type not in [
        SHAPEFILE,
        GEOPACKAGE,
    ]:
        raise ValueError(
            f"Unknown transfrom_to_type option: {transform_to_type}"
            f"Valid types: {SHAPEFILE, GEOPACKAGE, }"
        )
    if transform_to_type in [SHAPEFILE] and Path(output).is_file():
        if not len(inputs) == 1:
            raise ValueError(f"Shapefiles do not handle multiple layers.")


def finished(output):
    """
    Finish up by printing full path to output(s).
    """
    # TODO: click echo
    print(f"Output(s) were written to {output}.")


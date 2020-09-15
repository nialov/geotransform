"""
Description: Command line integration of geotransfrom.
"""
import click
from pathlib import Path

import geotrans.transform as transform
from geotrans.transform import (
    SHAPEFILE,
    GEOPACKAGE,
    FILEGEODATABASE,
    GEOJSON,
    driver_dict,
)


@click.command()
@click.argument(
    "inputs", type=click.Path(exists=True, readable=True, resolve_path=True), nargs=-1,
)
@click.option(
    "transform_to_type",
    "--to_type",
    type=click.Choice([SHAPEFILE, GEOPACKAGE, GEOJSON], case_sensitive=False),
    default=GEOPACKAGE,
    help="The spatial geodata filetype to transform to. Defaults to Geopackage.",
    show_default=True,
)
@click.option(
    "output",
    "--output",
    type=click.Path(writable=True, file_okay=True, dir_okay=True,),
    help="The output file or directory. "
    "Filename suffix is appended based on --to_type if missing from output.",
)
@click.version_option()
def main(inputs: tuple, transform_to_type: str, output: str):
    """
    A tool for transforming between spatial geodata filetypes
    (e.g. ESRI Shapefile, Geopackage).

    Inputs = File or files to transform to a type.
    Gathers all layers from all input files to the given output.

    A variable amount of input filenames are accepted, the type to transfrom
    the input to can be given and an output file or output directory can be
    given.

    If the output is a file:
    all layers are saved to that file if the given transform_to_type
    supports multiple layers.
    If the output is a directory all input layers are saved to that directory based
    on their layer name and the given --to_type parameter.
    """
    validate_inputs(inputs, transform_to_type, output)
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
    error_msg = (
        "Command line inputs did not match "
        "currently implemented functionality.\n"
        f"{inputs, transform_to_type, output}"
    )
    # Check that output filetype can handle saving.
    if transform_to_type in transform.SAVE_CAPABLE:
        # Check if output is a directory -> save to multiple individual files.
        if Path(output).exists() and Path(output).is_dir():
            click.echo(f"Saving to output folder: {output}")
            # Save individual geopackages, geojsons or shapefiles to a given directory.
            save_paths = []
            assert len(layer_names) != 0
            for layer_name in layer_names:
                save_paths.append(
                    Path(output) / Path(f"{layer_name}.{transform_to_type}")
                )

            assert len(save_paths) != 0
            transform.save_files(
                geodataframes, layer_names, save_paths, transform_to_type
            )
            finished(output)
        # Check if output is a single file that is also multilayer capable.
        elif (
            not Path(output).exists()
            and transform_to_type in transform.MULTILAYER_CAPABLE
        ):
            click.echo(f"Saving all layers to {output}")
            # Save a single geopackage output file with multiple layers
            # (if there are multiple layers in inputs).
            # Make sure file suffix is in the saved file.
            output = (
                output
                if f".{transform_to_type}" in output
                else f"{output}.{transform_to_type}"
            )
            transform.save_files(
                geodataframes, layer_names, [Path(output)], transform_to_type
            )
            finished(output)
        # Check if output is a single file and the output filetype does not
        # handle multilayer data.
        elif (
            not Path(output).exists()
            and transform_to_type not in transform.MULTILAYER_CAPABLE
            and len(geodataframes) == 1
        ):
            click.echo(f"Saving layer to {output}")
            output = (
                output
                if f".{transform_to_type}" in output
                else f"{output}.{transform_to_type}"
            )
            transform.save_files(
                geodataframes, layer_names, [Path(output)], transform_to_type
            )
            finished(output)
        # If file exists, overwriting is not currently not supported. -> error
        elif Path(output).is_file():
            raise FileExistsError(
                "Output file already exists. Overwriting curently not possible."
            )
        # If multilayer data has been read but output filetype does not support
        # multiple layers -> error
        elif (
            not Path(output).exists()
            and transform_to_type not in transform.MULTILAYER_CAPABLE
            and len(geodataframes) != 1
        ):
            raise TypeError(
                "Cannot save multilayer data to filetype that does not support"
                "multiple layers. Please give a directory to save"
                "files in individual type: {transform_to_type} files or "
                "use a multilayer capable filetype."
            )
        else:
            raise NotImplementedError(error_msg)

    else:
        raise NotImplementedError(error_msg)


def validate_inputs(inputs, transform_to_type: str, output: str) -> None:
    if any([argument is None for argument in (inputs, transform_to_type, output)]):
        raise TypeError(
            f"None value was passed as an argument.\n"
            f"Values: {inputs, transform_to_type, output}"
        )
    if not isinstance(inputs, tuple) or len(inputs) == 0:
        try:
            current_context = click.get_current_context()
            current_context.fail(
                "No inputs were given. Add --help to print help message."
            )
        except RuntimeError:
            print("No click runtime detected -> Script has been called from python.")
    if transform_to_type in [SHAPEFILE] and Path(output).is_file():
        if len(inputs) != 1:
            raise ValueError(f"Shapefiles do not handle multiple layers.")


def finished(output):
    """
    Finish up by printing full path to output(s).
    """
    # TODO: click echo
    # print(f"Output(s) were written to {output}.")
    click.echo(click.style(f"Layer data was written to {output}.", fg="green"))


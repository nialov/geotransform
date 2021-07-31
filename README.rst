Geotransformations Python Command Line Utility
==============================================

|Documentation Status| |PyPI Status| |CI Test| |Coverage|

Documentation
-------------

-  Published on ReadTheDocs:
   `Documentation <https://geotransform.readthedocs.io/en/latest/index.html>`__

Features
--------

-  Command line utility for easy transformations between geodata/spatial
   filetypes.
-  Python functions with documentation for direct usage.

   -  This is my own main use case: A package with all basic geopandas
      file loads and saves bundled.

-  Uses Python pathlib for cross-platform path handling.

Support
-------

Currently supports:

-  `GeoPackages <https://www.geopackage.org/>`__
-  `Esri
   Shapefiles <https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf>`__
-  `File
   Geodatabases <https://desktop.arcgis.com/en/arcmap/10.3/manage-data/administer-file-gdbs/file-geodatabases.htm>`__
   *Read only*
-  `GeoJSON <https://geojson.org/>`__

All file formats supported by geopandas can be implemented.

Dependencies
------------

-  `geopandas <https://github.com/geopandas/geopandas>`__ for
   transforming between geodata filetypes which in turn uses ``fiona`` (that
   uses ``GDAL``).
-  `click <https://github.com/pallets/click/>`__ for command line
   integration.

Alternatives
------------

The ``GDAL`` tool `ogr2ogr <https://gdal.org/programs/ogr2ogr.html>`__ is a
much more sophisticated command-line tool for converting between spatial
file formats.

Geopandas by itself supports many more spatial file formats. For more
advanced use cases when interacting with Python I recommend just using
geopandas.

Fiona provides a command-line interface ``fio``.
`fio <https://fiona.readthedocs.io/en/latest/manual.html>`__.

Installation
------------

-  PyPi

.. code:: bash

   pip install geotrans

-  poetry for development

.. code:: bash

   git clone https://github.com/nialov/geotransform.git
   cd geotransform
   poetry install

Using geotransform
------------------

Command line
~~~~~~~~~~~~

Run

.. code:: bash

   geotrans --help

to print the command line help for the utility.

To transform from a geopackage file with a single layer to an ESRI
shapefile:

.. code:: bash

   geotrans input_file.gpkg --to_type shp --output output_file.shp

To transform from a geopackage file with multiple layers to multiple
ESRI shapefiles into a given directory:

.. code:: bash

   geotrans input_file.gpkg --to_type shp --output output_dir

Python
~~~~~~

All main functions in charge of loading and saving geodata files are
exposed in the transform.py file in the geotrans package.

.. code:: python

   from geotrans.transform import load_file, save_files, SHAPEFILE_DRIVER
   from pathlib import Path

   # Your geodata file
   filepath = Path("input_file.gpkg")

   # load_file returns a single or multiple geodataframes depending
   # on how many layers are in the file.
   geodataframes, layer_names = load_file(filepath)

   # Assuming geopackage contained only one layer ->
   # Save acquired geodataframe and layer
   save_files(geodataframes, layer_names, [Path("output_file.shp")], SHAPEFILE_DRIVER)

License
-------

-  This project is licensed under the terms of the `MIT
   license. <LICENSE.md>`__

Copyright © 2020, Nikolas Ovaskainen.

.. |Documentation Status| image:: https://readthedocs.org/projects/geotransform/badge/?version=latest
   :target: https://geotransform.readthedocs.io/en/latest/?badge=latest
.. |PyPI Status| image:: https://img.shields.io/pypi/v/geotrans.svg
   :target: https://pypi.python.org/pypi/geotrans
.. |CI Test| image:: https://github.com/nialov/geotransform/workflows/test-and-publish/badge.svg
   :target: https://github.com/nialov/geotransform/actions/workflows/test-and-publish.yaml?query=branch%3Amaster
.. |Coverage| image:: https://raw.githubusercontent.com/nialov/geotransform/master/docs_src/imgs/coverage.svg
   :target: https://github.com/nialov/geotransform/blob/master/docs_src/imgs/coverage.svg

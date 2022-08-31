Geotransformations Python Command Line Utility
==============================================

|Documentation Status| |PyPI Status| |CI Test| |Coverage|

Current state
-------------

Currently archived as I have personally switched to just using
``ogr2ogr`` from ``gdal``. It has a difficult ``API`` on the
command-line but it implements such a vast array of functionality that
it is worth just learning.

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


Formatting and linting
----------------------


Formatting & linting:

.. code:: bash

   poetry run doit pre_commit
   poetry run doit lint

Building docs
-------------

Docs can be built locally to test that ``ReadTheDocs`` can also build them:

.. code:: bash

   poetry run doit docs

doit usage
----------

To list all available commands from ``dodo.py``:

.. code:: bash

   poetry run doit list

Development
~~~~~~~~~~~

Development dependencies for ``geotrans`` include:

-  ``poetry``

   -  Used to handle Python package dependencies.

   .. code:: bash

      # Use poetry run to execute poetry installed cli tools such as invoke,
      # nox and pytest.
      poetry run <cmd>


-  ``doit``

   -  A general task executor that is a replacement for a ``Makefile``
   -  Understands task dependencies and can run tasks in parallel
      even while running them in the order determined from dependencies
      between tasks. E.g. requirements.txt is a requirement for running
      tests and therefore the task creating requirements.txt will always
      run before the test task.

   .. code:: bash

      # Tasks are defined in dodo.py
      # To list doit tasks from command line
      poetry run doit list
      # To run all tasks in parallel (recommended before pushing and/or
      # committing)
      # 8 is the number of cpu cores, change as wanted
      # -v 0 sets verbosity to very low. (Errors will always still be printed.)
      poetry run doit -n 8 -v 0

-  ``nox``

   -  ``nox`` is a replacement for ``tox``. Both are made to create
      reproducible Python environments for testing, making docs locally, etc.

   .. code:: bash

      # To list available nox sessions
      # Sessions are defined in noxfile.py
      poetry run nox --list

-  ``copier``

   -  ``copier`` is a project templater. Many Python projects follow a similar
      framework for testing, creating documentations and overall placement of
      files and configuration. ``copier`` allows creating a template project
      (e.g. https://github.com/nialov/nialov-py-template) which can be firstly
      cloned as the framework for your own package and secondly to pull updates
      from the template to your already started project.

   .. code:: bash

      # To pull copier update from github/nialov/nialov-py-template
      poetry run copier update


-  ``pytest``

   -  ``pytest`` is a Python test runner. It is used to run defined tests to
      check that the package executes as expected. The defined tests in
      ``./tests`` contain many regression tests (done with
      ``pytest-regressions``) that make it almost impossible
      to add features to ``geotrans`` that changes the results of functions
      and methods.

   .. code:: bash

      # To run tests implemented in ./tests directory and as doctests
      # within project itself:
      poetry run pytest


-  ``coverage``

   .. code:: bash

      # To check coverage of tests
      # (Implemented as nox session!)
      poetry run nox --session test_pip

-  ``sphinx``

   -  Creates documentation from files in ``./docs_src``.

   .. code:: bash

      # To create documentation
      # (Implemented as nox session!)
      poetry run nox --session docs

Big thanks to all maintainers of the above packages!

License
-------

-  This project is licensed under the terms of the `MIT
   license. <LICENSE.md>`__

Copyright © 2020, Nikolas Ovaskainen.

-----


.. |Documentation Status| image:: https://readthedocs.org/projects/geotransform/badge/?version=latest
   :target: https://geotransform.readthedocs.io/en/latest/?badge=latest
.. |PyPI Status| image:: https://img.shields.io/pypi/v/geotrans.svg
   :target: https://pypi.python.org/pypi/geotrans
.. |CI Test| image:: https://github.com/nialov/geotransform/workflows/test-and-publish/badge.svg
   :target: https://github.com/nialov/geotransform/actions/workflows/test-and-publish.yaml?query=branch%3Amaster
.. |Coverage| image:: https://raw.githubusercontent.com/nialov/geotransform/master/docs_src/imgs/coverage.svg
   :target: https://github.com/nialov/geotransform/blob/master/docs_src/imgs/coverage.svg

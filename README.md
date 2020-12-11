# Geotransformations Python Command Line Utility

## Documentation

* Published on ReadTheDocs:
  [Documentation](https://geotransform.readthedocs.io/en/latest/index.html)

## Features

* Command line utility for easy transformations between geodata/spatial
  filetypes.
* Python functions with documentation for direct usage.
  * This is my own main use case: A package with all basic geopandas file loads
    and saves bundled.
* Uses Python pathlib for cross-platform path handling.

## Support

Currently supports:

* [GeoPackages](https://www.geopackage.org/)
* [Esri
  Shapefiles](https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf)
* [File
  Geodatabases](https://desktop.arcgis.com/en/arcmap/10.3/manage-data/administer-file-gdbs/file-geodatabases.htm)
  *Read only*
* [GeoJSON](https://geojson.org/)

All file formats supported by geopandas can be implemented.

## Dependencies

* [geopandas](https://github.com/geopandas/geopandas) for transforming between
  geodata filetypes which in turn uses fiona (that uses GDAL).
* [click](https://github.com/pallets/click/) for command line integration.

## Alternatives

The GDAL tool [ogr2ogr](https://gdal.org/programs/ogr2ogr.html) is a much more
sophisticated command-line tool for converting between spatial file formats.

Geopandas by itself supports many more spatial file formats. For more advanced
use cases when interacting with Python I recommend just using geopandas.

Fiona provides a command-line interface *fio*.
[fio](https://fiona.readthedocs.io/en/latest/manual.html).

## License

* This project is licensed under the terms of the [MIT license.](LICENSE.md)

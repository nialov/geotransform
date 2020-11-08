# Module installation

* Installation works well on linux.
* Installation of e.g. GDAL will fail with windows pip install.
  * On windows installing e.g. GDAL from
    [Gohlke's](https://www.lfd.uci.edu/~gohlke/pythonlibs/) pre-built binaries
    is often recommended as the easiest method.

## From PyPI source

* pip installation:

~~~bash
# Add --user for user specific installation
pip install geotrans --user
~~~

* pipenv installation:
  * Requires Python >3.7 installed with
    [pipenv](https://pipenv.pypa.io/en/latest/)

~~~bash
pipenv install geotrans
~~~

## From GitHub source

* pip installation:

~~~bash
# Manually using git
git clone https://github.com/nialov/geotransform.git --depth 1
cd geotransform
pip3 install .

# Using pip+git
pip install git+https://github.com/nialov/geotransform#egg=geotrans
~~~

* pipenv installation:

Pipenv allows exact replication of python environment using the Pipfile.lock
file. `pipenv sync` installs from the Pipfile.lock.

~~~bash
git clone https://github.com/nialov/geotransform.git --depth 1
cd geotransform
pipenv sync
pipenv shell
~~~

* pipenv installation for development:
  * This is the preferred installation for development purposes.

~~~bash
git clone https://github.com/nialov/geotransform.git
cd geotransform
pipenv sync --dev
# Run tests with tox
pipenv run tox -e py37, py38
# Make documentation locally
pipenv run tox -e docs
~~~

# Test installation

* Script accessible as geotrans

~~~bash
# With pip installation
geotrans --help
# With pipenv
pipenv run geotrans --help
# or
pipenv shell
# now in geotrans shell (geotrans)
geotrans --help
~~~

# Module installation

## Install into your Python environment of choice with pip

Both methods use the included setup.py to install the package.

~~~bash
# Manually using git
git clone https://github.com/nialov/geotransform.git --depth 1
cd geotransform
pip3 install .

# Using pip+git
pip install git+https://github.com/nialov/geotransform#egg=geotrans
~~~

## From source into pipenv

* Requires Python >3.7 installed with
  [pipenv](https://pipenv.pypa.io/en/latest/)

Pipenv allows exact replication of python environment using the Pipfile.lock
file. `pipenv sync` installs from the Pipfile.lock.

~~~bash
git clone https://github.com/nialov/geotransform.git --depth 1
cd geotransform
pipenv sync
pipenv shell
~~~

If you want to run tests or make documentation add --dev after pipenv
sync. tox runs the test suite, makes documentation and syncs Pipfile
-> setup.py files.

~~~bash
pipenv sync --dev
pipenv shell
tox
~~~

Script now accessible as geotrans inside the pipenv

~~~bash
geotrans --help
~~~

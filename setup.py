from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    extras_require={
        "dev": [
            "alabaster==0.7.12",
            "appdirs==1.4.4",
            "attrs==20.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "babel==2.8.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "black==19.10b0; python_version >= '3.6'",
            "cached-property==1.5.1",
            "cerberus==1.3.2",
            "certifi==2020.6.20",
            "chardet==3.0.4",
            "click==7.1.2",
            "colorama==0.4.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "commonmark==0.9.1",
            "distlib==0.3.1",
            "docutils==0.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "filelock==3.0.12",
            "hypothesis==5.30.0",
            "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "imagesize==1.2.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "iniconfig==1.0.1",
            "jinja2==2.11.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "more-itertools==8.5.0; python_version >= '3.5'",
            "orderedmultidict==1.0.1",
            "packaging==20.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pathspec==0.8.0",
            "pbr==5.4.5",
            "pep517==0.8.2",
            "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "pipenv==2020.8.13; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pipenv-setup==3.1.1",
            "pipenv-to-requirements==0.9.0",
            "pipfile==0.0.2",
            "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pluggy==0.13.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "py==1.9.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pygments==2.6.1; python_version >= '3.5'",
            "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pytest==6.0.1",
            "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pytz==2020.1",
            "recommonmark==0.6.0",
            "regex==2020.7.14",
            "requests==2.24.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "requirementslib==1.5.13; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "snowballstemmer==2.0.0",
            "sortedcontainers==2.2.2",
            "sphinx==3.2.1",
            "sphinx-autodoc-typehints==1.11.0",
            "sphinxcontrib-applehelp==1.0.2; python_version >= '3.5'",
            "sphinxcontrib-devhelp==1.0.2; python_version >= '3.5'",
            "sphinxcontrib-htmlhelp==1.0.3; python_version >= '3.5'",
            "sphinxcontrib-jsmath==1.0.1; python_version >= '3.5'",
            "sphinxcontrib-qthelp==1.0.3; python_version >= '3.5'",
            "sphinxcontrib-serializinghtml==1.1.4; python_version >= '3.5'",
            "toml==0.10.1",
            "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "tox==3.19.0",
            "typed-ast==1.4.1",
            "urllib3==1.25.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
            "virtualenv==20.0.31; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "virtualenv-clone==0.5.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "wheel==0.35.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        ]
    },
    name="geotrans",
    version="0.1",
    author="Nikolas Ovaskainen",
    author_email="nikolasovaskainen@gmail.com",
    description="Fast geodata filetype transformations using geopandas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        "attrs==20.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "click==7.1.2",
        "click-plugins==1.1.1",
        "cligj==0.5.0",
        "fiona==1.8.13.post1",
        "geopandas==0.8.1",
        "munch==2.5.0",
        "numpy==1.19.1; python_version >= '3.6'",
        "pandas==1.1.1; python_full_version >= '3.6.1'",
        "pyproj==2.6.1.post1; python_version >= '3.5'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.1",
        "shapely==1.7.1",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    ],
    test_require=["pytest", "sphinx", "recommonmark"],
    dependency_links=[],
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        geotrans=geotrans.cli:main
    """,
)

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    extras_require={
        "dev": [
            "hypothesis",
            "pytest",
            "sphinx",
            "recommonmark",
            "tox",
            "pipenv-setup",
            "pipenv-to-requirements",
            "pylama",
            "setuptools",
            "wheel",
            "twine",
            "bump2version",
            "invoke",
            "sphinx-rtd-theme",
            "nox",
            "coverage",
        ]
    },
    name="geotrans",
    version="0.0.4",
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
    install_requires=["geopandas", "click"],
    test_require=[],
    dependency_links=[],
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        geotrans=geotrans.cli:main
    """,
)

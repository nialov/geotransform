from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
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
    install_requires=["click", "geopandas"],
    entry_points="""
        [console_scripts]
        geotrans=geotrans.cli:main
    """,
)

from setuptools import setup, find_packages

setup(
    name="geotrans",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "geopandas"],
    entry_points="""
        [console_scripts]
        geotrans=geotrans.cli:main
    """,
)
# cat: pipfile: No such file or directory
# [[source]]
# name = "pypi"
# url = "https://pypi.org/simple"
# verify_ssl = true

# [dev-packages]
# hypothesis = "*"
# pytest = "*"
# sphinx = "*"

# [packages]
# geopandas = "*"
# click = "*"

# [requires]
# python_version = "3.8"

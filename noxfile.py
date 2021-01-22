"""
Nox test suite.
"""

import os
from pathlib import Path
from shutil import copy2, copytree, rmtree

from setuptools import find_packages

import nox


docs_apidoc_dir_path = Path("docs_src/apidoc")
docs_dir_path = Path("docs")


@nox.session(python="3.8")
def pipenv_sync_test(session: nox.Session):
    """
    Run strict pipenv test suite.

    Creates tmp directory where Pipenv will sync dependencies from Pipfile.lock
    """
    tmp_dir = session.create_tmp()
    for to_copy in (*find_packages("."), "Pipfile.lock"):
        if Path(to_copy).is_dir():
            copytree(to_copy, Path(tmp_dir) / to_copy)
        elif Path(to_copy).is_file():
            copy2(to_copy, tmp_dir)
        elif Path(to_copy).exists():
            ValueError("File not dir or file.")
        else:
            FileNotFoundError("Expected file to be found.")
    session.chdir(tmp_dir)
    session.install("pipenv")
    session.run("pipenv", "sync", "--python", f"{session.python}", "--dev", "--bare")
    session.run(
        "pipenv",
        "run",
        "coverage",
        "run",
        "--include",
        "geotrans/**.py",
        "-m",
        "pytest",
    )
    session.run("pipenv", "run", "coverage", "report", "--fail-under", "70")


@nox.session(python=["3.7", "3.8"])
def tests_lazy(session):
    """
    Run lazy test suite.
    """
    session.install(".[dev]")
    session.run("pytest")
    # test that geotrans cli tool is installed (and responding)
    session.run("geotrans", "--help")


@nox.session
def rstcheck_docs(session):
    """
    Check docs_src with rstcheck.
    """
    session.install("rstcheck", "sphinx")
    session.run(
        "rstcheck", "-r", "docs_src", "--ignore-directives", "automodule",
    )


@nox.session
def docs(session):
    """
    Make documentation.

    Installation mimics readthedocs install (if succeeds, RTD should succeed.).
    """
    session.install(".[dev]")
    if docs_apidoc_dir_path.exists():
        rmtree(docs_apidoc_dir_path)
    if docs_dir_path.exists():
        rmtree(docs_dir_path)
    session.run("sphinx-apidoc", "-o", "./docs_src/apidoc", "./geotrans", "-e", "-f")
    session.run(
        "sphinx-build", "./docs_src", "./docs", "-b", "html",
    )


"""
Nox test suite.
"""

from pathlib import Path
from shutil import copy2, copytree, rmtree

import nox


docs_apidoc_dir_path = Path("docs_src/apidoc")
docs_dir_path = Path("docs")


@nox.session(python="3.8")
def teest(session):
    """
    Run strict test suite.
    """
    session.run("pwd")


@nox.session(python="3.8")
def tests_strict(session: nox.Session):
    """
    Run strict test suite.
    """
    tmp_dir = session.create_tmp()
    for to_copy in ("geotrans", "tests", "Pipfile.lock"):
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
    session.run(*"pipenv sync --dev --bare".split(" "))
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


@nox.session
def test_geotrans(session):
    """
    Run test on geotrans script in new virtualenv.
    """
    session.install(".")
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

    Installation mimics readthedocs install.
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


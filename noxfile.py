"""
Nox test suite.
"""
from pathlib import Path
from shutil import rmtree
from typing import List

import nox

CHANGELOG_PATH = Path("CHANGELOG.md")
CITATION_CFF_PATH = Path("CITATION.cff")
DOCS_SRC_PATH = Path("docs_src")
COVERAGE_SVG_PATH = DOCS_SRC_PATH / Path("imgs/coverage.svg")
DEFAULT_PYTHON_VERSION = "3.8"
DEV_REQUIREMENTS_PATH = Path("requirements.txt")
DOCS_EXAMPLES_PATH = Path("examples")
README_PATH = Path("README.rst")
DOCS_FILES = [*list(DOCS_SRC_PATH.rglob("*.rst")), README_PATH]
DOCS_PATH = Path("docs")
DOCS_REQUIREMENTS_PATH = Path("docs_src/requirements.txt")
DOCS_SRC_PATH = Path("docs_src")
DODO_PATH = Path("dodo.py")
NOTEBOOKS_PATH = DOCS_SRC_PATH / "notebooks"
NOTEBOOKS = [
    *list(NOTEBOOKS_PATH.rglob("*.ipynb")),
]
NOXFILE_PATH = Path("noxfile.py")
PACKAGE_NAME = "geotrans"
PYTHON_VERSIONS = ["3.7", "3.8", "3.9"]
TESTS_PATH = Path("tests")
UTF8 = "utf-8"

DOCS_APIDOC_DIR_PATH = DOCS_SRC_PATH / "apidoc"
PROFILE_SCRIPT_PATH = Path("tests/_profile.py")
TASKS_PATH = Path("tasks.py")
DOCS_AUTO_EXAMPLES_PATH = Path("docs_src/auto_examples")


VENV_PARAMS = dict(venv_params=["--copies"])


def filter_paths_to_existing(*iterables: Path) -> List[Path]:
    """
    Filter paths to only existing.
    """
    return [path for path in iterables if path.exists()]


def execute_notebook(session, notebook: Path):
    """
    Execute notebook.
    """
    session.run(
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--inplace",
        "--execute",
        str(notebook),
    )
    # Strip output
    session.run(
        "nbstripout",
        str(notebook),
    )
    # Strip output
    session.run(
        "nbstripout",
        str(notebook),
    )


def install_dev(session, extras: str = ""):
    """
    Install all package and dev dependencies.
    """
    session.install(f".{extras}")
    session.install("-r", str(DEV_REQUIREMENTS_PATH))


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True, **VENV_PARAMS)
def tests_pip(session):
    """
    Run test suite with pip install.
    """
    # Check if any tests exist
    if (
        not TESTS_PATH.exists()
        or TESTS_PATH.is_file()
        or len(list(TESTS_PATH.iterdir())) == 0
    ):
        print(f"No tests in {TESTS_PATH} directory.")
        return

    # Install dependencies dev + coverage
    install_dev(session=session, extras="[coverage]")

    # Test with pytest and determine coverage
    session.run("coverage", "run", "--source", PACKAGE_NAME, "-m", "pytest")

    # Fails with test coverage under 70
    session.run("coverage", "report", "--fail-under", "70")

    assert session.python in PYTHON_VERSIONS
    if session.python == DEFAULT_PYTHON_VERSION:
        # Make coverage-badge image
        if COVERAGE_SVG_PATH.exists():
            COVERAGE_SVG_PATH.unlink()
        elif not COVERAGE_SVG_PATH.parent.exists():
            COVERAGE_SVG_PATH.parent.mkdir(parents=True)
        session.run("coverage-badge", "-f", "-o", str(COVERAGE_SVG_PATH))

    # Test that entrypoint works.
    session.run(PACKAGE_NAME.replace("_", "-"), "--help")


def resolve_session_posargs(session):
    """
    Resolve session.posargs.
    """
    # Default
    value = ""
    if session.posargs:
        if isinstance(session.posargs, str):
            value = session.posargs
        elif isinstance(session.posargs, (tuple, list)):
            value = session.posargs[0]
        else:
            raise TypeError(
                f"Expected (str,tuple,list) as posargs type. Got: {type(session.posargs)}"
                f" with contents: {session.posargs}."
            )
    return value


@nox.session(python=DEFAULT_PYTHON_VERSION, **VENV_PARAMS, reuse_venv=True)
def notebooks(session):
    """
    Run notebooks.

    Notebooks are usually run in remote so use pip install. Note that notebooks
    shouldn't have side effects i.e. disk file writing.
    """
    # Check if any notebooks exist.
    if len(NOTEBOOKS) == 0:
        print("No notebooks found.")
        return

    # Install dev dependencies
    install_dev(session=session)

    # Test notebook(s)
    for notebook_path in NOTEBOOKS:
        execute_notebook(session=session, notebook=notebook_path)


def setup_format_and_lint(session) -> List[str]:
    existing_paths = filter_paths_to_existing(
        Path(PACKAGE_NAME),
        TESTS_PATH,
        TASKS_PATH,
        NOXFILE_PATH,
        DODO_PATH,
        DOCS_EXAMPLES_PATH,
    )

    if len(existing_paths) == 0:
        print("Nothing to format.")

    # Install formatting and lint dependencies
    install_dev(session=session, extras="[format-lint]")
    return [str(path) for path in existing_paths]


@nox.session(reuse_venv=True, **VENV_PARAMS)
def format(session):
    """
    Format python files, notebooks and docs_src.
    """
    existing_paths = setup_format_and_lint(session=session)

    # Format python files
    session.run("black", *existing_paths)

    # Format python file imports
    session.run(
        "isort",
        *existing_paths,
    )

    # Format notebooks with black (must be installed with black[jupyter])
    for notebook in NOTEBOOKS:
        session.run("black", str(notebook))

    # Format code blocks in documentation files
    session.run("blacken-docs", *[str(path) for path in DOCS_FILES], str(README_PATH))

    # Format code blocks in Python files
    session.run(
        "blackdoc",
        *existing_paths,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def lint(session):
    """
    Lint python files, notebooks and docs_src.
    """
    existing_paths = setup_format_and_lint(session=session)

    # Lint docs
    session.run(
        "rstcheck",
        "-r",
        "docs_src",
        "--ignore-directives",
        "automodule",
    )

    # Lint Python files with black (all should be formatted.)
    session.run("black", "--check", *existing_paths)

    for notebook in NOTEBOOKS:
        # Lint notebooks with black (all should be formatted.)
        session.run("black", "--check", str(notebook))

    # Lint imports
    session.run(
        "isort",
        "--check-only",
        *existing_paths,
    )

    # Lint with pylint
    session.run(
        "pylint",
        *existing_paths,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def format_and_lint(session):
    """
    Format and lint python files, notebooks and docs_src.
    """
    existing_paths = setup_format_and_lint(session=session)

    if len(existing_paths) == 0:
        print("Nothing to format or lint.")
        return

    # Install formatting and lint dependencies
    install_dev(session=session, extras="[format-lint]")

    # Format python files
    session.run("black", *existing_paths)

    # Format python file imports
    session.run(
        "isort",
        *existing_paths,
    )

    # Format notebooks with black (must be installed with black[jupyter])
    for notebook in NOTEBOOKS:
        session.run("black", str(notebook))

    # Format code blocks in documentation files
    session.run(
        "blacken-docs",
        README_PATH,
        *[str(path) for path in DOCS_FILES],
    )

    # Format code blocks in Python files
    session.run(
        "blackdoc",
        *existing_paths,
    )

    # Lint docs
    session.run(
        "rstcheck",
        "-r",
        "docs_src",
        "--ignore-directives",
        "automodule",
    )

    # Lint Python files with black (all should be formatted.)
    session.run("black", "--check", *existing_paths)

    for notebook in NOTEBOOKS:
        # Lint notebooks with black (all should be formatted.)
        session.run("black", "--check", str(notebook))

    session.run(
        "isort",
        "--check-only",
        *existing_paths,
    )

    # Lint with pylint
    session.run(
        "pylint",
        *existing_paths,
    )


@nox.session(reuse_venv=True, **VENV_PARAMS)
def requirements(session):
    """
    Sync poetry requirements from pyproject.toml to requirements.txt.
    """
    # Install poetry
    session.install("poetry")

    # Sync dev requirements
    session.run(
        "poetry",
        "export",
        "--without-hashes",
        "--dev",
        "-o",
        str(DEV_REQUIREMENTS_PATH),
    )

    # Sync docs requirements
    session.run(
        "poetry",
        "export",
        "--without-hashes",
        "--dev",
        "-E",
        "docs",
        "-o",
        str(DOCS_REQUIREMENTS_PATH),
    )


def _docs(session, auto_build: bool):
    """
    Make documentation.

    Installation mimics readthedocs install.
    """
    # Install from docs_src/requirements.txt that has been synced with docs
    # requirements
    session.install(".")
    session.install("-r", str(DOCS_REQUIREMENTS_PATH))

    # Remove old apidocs
    if DOCS_APIDOC_DIR_PATH.exists():
        rmtree(DOCS_APIDOC_DIR_PATH)

    # Remove all old docs
    if DOCS_PATH.exists():
        rmtree(DOCS_PATH)

    # Create apidocs
    session.run(
        "sphinx-apidoc", "-o", "./docs_src/apidoc", f"./{PACKAGE_NAME}", "-e", "-f"
    )

    try:
        # Create docs in ./docs folder
        session.run(
            "sphinx-build" if not auto_build else "sphinx-autobuild",
            str(DOCS_SRC_PATH),
            str(DOCS_PATH),
            *(
                [
                    "--open-browser",
                    f"--ignore=**/{DOCS_AUTO_EXAMPLES_PATH.name}/**",
                    "--watch=README.rst",
                    f"--watch={PACKAGE_NAME}/",
                    "--watch=examples/",
                ]
                if auto_build
                else []
            ),
        )

    finally:
        # Clean up sphinx-gallery folder in ./docs_src/auto_examples
        if DOCS_AUTO_EXAMPLES_PATH.exists():
            rmtree(DOCS_AUTO_EXAMPLES_PATH)


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def docs(session):
    """
    Make documentation.

    Installation mimics readthedocs install.
    """
    _docs(session=session, auto_build=False)


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def auto_docs(session):
    """
    Make documentation and start sphinx-autobuild service.
    """
    _docs(session=session, auto_build=True)


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def update_version(session):
    """
    Update package version from git vcs.
    """
    # Install poetry-dynamic-versioning
    session.install("poetry-dynamic-versioning")

    # Run poetry-dynamic-versioning to update version tag in pyproject.toml
    # and geotrans/__init__.py
    session.run("poetry-dynamic-versioning")


@nox.session(reuse_venv=True, python=PYTHON_VERSIONS, **VENV_PARAMS)
def build(session):
    """
    Build package with poetry.
    """
    # Install poetry
    session.install("poetry")

    # Install dependencies to poetry
    session.run("poetry", "install")

    # Build
    session.run("poetry", "build")


@nox.session(reuse_venv=True, **VENV_PARAMS)
def profile_performance(session):
    """
    Profile geotrans runtime performance.

    User must implement the actual performance utility.
    """
    # Install dev and pyinstrument
    install_dev(session)
    session.install("pyinstrument")

    # Create temporary path
    save_file = f"{session.create_tmp()}/profile_runtime.html"

    if not PROFILE_SCRIPT_PATH.exists():
        raise FileNotFoundError(
            f"Expected {PROFILE_SCRIPT_PATH} to exist for performance profiling."
        )

    # Run pyprofiler
    session.run(
        "pyinstrument",
        "--renderer",
        "html",
        "--outfile",
        save_file,
        str(PROFILE_SCRIPT_PATH),
    )

    resolved_path = Path(save_file).resolve()
    print(f"\nPerformance profile saved at {resolved_path}.")


@nox.session(reuse_venv=True, **VENV_PARAMS)
def typecheck(session):
    """
    Typecheck Python code.
    """
    # Install package and typecheck dependencies
    install_dev(session=session, extras="[typecheck]")

    # Format python files
    session.run("mypy", PACKAGE_NAME)


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def validate_citation_cff(session):
    """
    Validate CITATION.cff.

    From: https://github.com/citation-file-format/citation-file-format
    """
    # Path to CITATION.cff
    citation_cff_path = CITATION_CFF_PATH.absolute()

    # create temporary directory and chdir there
    tmp_dir = session.create_tmp()
    session.chdir(tmp_dir)

    # Remove existing dir
    citation_file_format_dir = Path("citation-file-format")
    if citation_file_format_dir.exists():
        rmtree(citation_file_format_dir)

    # clone this repository and chdir into the repo
    session.run(
        "git",
        "clone",
        "https://github.com/citation-file-format/citation-file-format.git",
        "--depth",
        "1",
        external=True,
    )
    session.chdir(str(citation_file_format_dir))

    # install the validation dependencies in user space
    session.install("ruamel.yaml", "jsonschema")

    # run the validator on your CITATION.cff
    session.run(
        "python3",
        str(Path("examples/validator.py")),
        "-s",
        "schema.json",
        "-d",
        str(citation_cff_path),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True, **VENV_PARAMS)
def changelog(session):
    """
    Create CHANGELOG.md.
    """
    version = resolve_session_posargs(session=session)
    assert isinstance(version, str)

    # Path to changelog.md
    changelog_path = CHANGELOG_PATH.absolute()

    # Check if pandoc is installed
    pandoc_installed = True
    try:
        session.run("pandoc", "--help", external=True)
    except Exception:
        pandoc_installed = False
        print("Expected 'pandoc' to be installed. Cannot generate clean changelog.")

    # Install auto-changelog from own repo
    session.install("git+https://github.com/nialov/auto-changelog.git")
    session.run(
        "auto-changelog",
        "--tag-prefix=v",
        f"--output={str(CHANGELOG_PATH)}",
        f"--latest-version={version}" if len(version) > 0 else "--unreleased",
    )

    # Add empty lines after each line of changelog
    new_lines = []
    for line in changelog_path.read_text(encoding=UTF8).splitlines():
        # Also remove quadruple hashes
        new_lines.append(line.replace("####", "###"))
        new_lines.append("")

    changelog_path.write_text("\n".join(new_lines), encoding=UTF8)
    if pandoc_installed:
        session.run(
            "pandoc",
            str(CHANGELOG_PATH),
            "--from",
            "markdown",
            "--to",
            "markdown",
            "--output",
            str(CHANGELOG_PATH),
            external=True,
        )
    print(changelog_path.read_text(encoding=UTF8))

    assert changelog_path.exists()


@nox.session(reuse_venv=True, **VENV_PARAMS)
def codespell(session):
    """
    Check spelling in code.
    """
    session.install("codespell")
    session.run("codespell", PACKAGE_NAME, str(DOCS_EXAMPLES_PATH))

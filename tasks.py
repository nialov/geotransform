from invoke import task

patch = "patch"
minor = "minor"
major = "major"

make_dist_cmd = "pipenv run python3 setup.py sdist bdist_wheel"


@task
def make_pytest(c):
    c.run("pipenv run pytest")


@task
def make_tox(c):
    c.run("pipenv run tox -e py37, py38")


@task
def make_pipenv_requirements(c):
    c.run("pipenv run pipenv_to_requirements")
    c.run("pipenv run pipenv-setup sync --dev")


@task
def make_tox_docs(c):
    c.run("pipenv run tox -e docs")


@task
def make_dist(c):
    c.run(make_dist_cmd)


def git_commit_all(c, commit_msg: str) -> int:
    c.run("git add .")
    result = c.run(f"git commit -m '{commit_msg}'")
    return result.exited


@task(
    help={"patch_minor_major": "Patch, minor or major version bump."},
    pre=[make_pytest, make_tox, make_pipenv_requirements, make_tox_docs],
    post=[make_pytest],
)
def make_version_bump(c, patch_minor_major=patch):
    git_commit_all(c, commit_msg="Git commit before version bump.")
    c.run(f"bump2version --verbose {patch_minor_major} --dry-run")
    c.run(make_dist_cmd)
    git_commit_all(c, commit_msg="Git commit after version bump and make_dist.")

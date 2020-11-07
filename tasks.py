from invoke import task
import re

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
    # Add -f for applications
    c.run("pipenv run pipenv_to_requirements -f")
    c.run("pipenv run pipenv-setup sync --dev")


# @task
# def make_tox_docs(c):
#     c.run("pipenv run tox -e docs")


@task
def make_dist(c):
    c.run(make_dist_cmd)


def git_commit_all(c, commit_msg: str) -> int:
    c.run("git add .")
    result = c.run(f"git commit -m '{commit_msg}'")
    return result.exited


@task(
    help={"patch_minor_major": "Patch, minor or major version bump."},
    pre=[make_pytest, make_tox, make_pipenv_requirements],
    post=[make_pytest, make_dist],
)
def make_version_bump(c, patch_minor_major=patch):
    verify = input(
        f"Are you sure you wish to do a {patch_minor_major} version bump? y/n: "
    )
    if verify not in ["y", "yes", "Y"]:
        print(f"Aborting according to user input: {verify}")
        return
    git_commit_all(c, commit_msg="Git commit before version bump.")
    c.run(f"bump2version --verbose {patch_minor_major}")


@task
def make_tagged_commit(c):
    with open(".bumpversion.cfg") as cfg:
        curr_version_line = [
            line for line in cfg.readlines() if "current_version = " in line
        ]
        assert len(curr_version_line) == 1
        curr_version_line: str = curr_version_line[0]
        print(curr_version_line.strip())
        pattern = re.compile("\d")
        match = re.match(pattern, curr_version_line)
        print(match)

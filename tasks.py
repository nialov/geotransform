from invoke import task

patch = "patch"
minor = "minor"
major = "major"


def git_commit_all(c, commit_msg: str) -> int:
    c.run("git add .")
    result = c.run(f"git commit -m '{commit_msg}'")
    return result.exited


@task(help={"patch_minor_major": "Patch, minor or major version bump."})
def make_version_bump(c, patch_minor_major=patch):
    if patch_minor_major not in (patch, minor, major):
        print("Incorrect patch_minor_major argument.")
        print(f"Correct choices: {(patch, minor, major)}")
        return
    result = c.run("pipenv run tox")
    if result.exited == 0:
        # tox succesfully exited
        git_commit_all(c, commit_msg="tox build before bumping version")
        bump_result = c.run(f"bump2version --verbose {patch_minor_major} --dry-run")
        if bump_result.exited == 0:
            c.run("pipenv run tox")
            git_commit_all(c, commit_msg="tox build after bumping version.")
            print("All committed and ready for git push.")
        else:
            return
    else:
        return

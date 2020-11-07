from invoke import task

patch = "patch"
minor = "minor"
major = "major"


@task(help={"patch_minor_major": "Patch, minor or major version bump."})
def make_version_bump(c, patch_minor_major=patch):
    if patch_minor_major not in (patch, minor, major):
        print("Incorrect patch_minor_major argument.")
        print(f"Correct choices: {(patch, minor, major)}")
    fail_msg = "-> Failed to bump version."
    print("Running tox.")
    result = c.run("pipenv run tox")
    print("Tox exited with:")
    print(result.exited)
    if result.exited == 0:
        # tox succesfully exited
        print("Tox succesfull.")
        print("Creating git commit.")
        c.run("git add .")
        c.run("git commit -m 'tox build before bumping version'")
        print(f"Running bump2version with {patch_minor_major} as bump.")
        bump_result = c.run(f"bump2version --verbose {patch_minor_major} --dry-run")
        if bump_result == 0:
            print("Succesful bump.")
        else:
            print(fail_msg)
    else:
        print("Tox failed.")
        print(fail_msg)

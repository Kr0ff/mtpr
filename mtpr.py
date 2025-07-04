#!/usr/bin/env python3

import os
import sys
import json
import pathlib

try:
    import git # GitPython
    import argparse

except ImportError as e:
    raise Exception(f"[-] Missing required python library - \n {e}")

# Check if provided argument is a file
def isfile(json_file):

    file = False

    if os.path.isfile(json_file):
        file = True

    return file

# Is the package a git repo to clone ?
def ispackage_git(_json):

    _isgit = False

    _dump = json.dumps(_json)

    _json = json.loads(_dump)

    if _json["git"] == True:
        _isgit = True

    return _isgit

# parse the json file with package
def parseJson(json_file):

    _json = ""

    # Do file check
    check_isfile = isfile(json_file)
    if check_isfile == False:
        print("[-] Specified argument is not a file")
        sys.exit(-1)

    # Resolve the file location
    json_file = pathlib.Path(json_file).resolve()

    # open the package file
    with open(json_file, "r") as _package:
        _json = json.load(_package)

    return _json

# Check package category and clone to specific folder
def getcategory_repo(_json):

    _category = ""

    _dump = json.dumps(_json)

    _json = json.loads(_dump)
    if not _json["category"]:
        print("[-] Category field not provided or empty in JSON packages file")
        sys.exit(1)
    else:
        _category = _json["category"]

    return _category

def repo_folder_exists(_location):

    # Store result
    _bResult = False

    _pathObj = pathlib.Path(_location)

    # Store the repo
    if _pathObj.exists():
        _bResult = True

    return _bResult

# Performs the cloning of repos
def gitcloner(json_file):

    # Disable prompting of credentials for when
    # The owner has set a repository as private
    # --------------------
    os.environ["GIT_TERMINAL_PROMPT"] = "0"

    print(f"[+] Starting repository cloning - ({json_file})")

    _json = parseJson(json_file)

    _package_ = ""

    _not_git_package = []
    _unsuccessfully_cloned = []

    # Loop through all packages in the package.json file
    for repo in _json:
        _package_ = _json[repo]

        _git_check_repo_category = getcategory_repo(_package_)
        if not _git_check_repo_category:
            print("[-] No repository category specified")
            sys.exit(1)

        # Check if package is clonable (git valid)
        _git_check = ispackage_git(_package_)
        if _git_check == True:

            # Set the vars for each attribute of a package
            _git_repo_name = _package_["name"]
            _git_url = _package_["url"]
            _git_clone_location = _package_["location"]
            _git_repo_category = _package_["category"]

            _cloned_repo_location = f"{_git_clone_location}{_git_repo_category}/{_git_repo_name}"

            # Do cloning of repo
            try:

                try:
                    # Check the repository doesn't already exists/is cloned
                    if not repo_folder_exists(_cloned_repo_location):
                        print(f"\t+ [ {_git_repo_name} ]", end="", flush=True)
                        _clone = git.Repo.clone_from(_git_url, _cloned_repo_location)
                        if _clone:
                            print(" -> Cloned !")
                    else:
                        # Skip repo is already cloned
                        continue
                except git.exc.GitCommandError as gE:
                    if 'Authentication failed' in str(gE) or 'Repository not found' in str(gE):
                        _unsuccessfully_cloned.append(_package_["name"])
                        continue

            # Cancel if ctrl+c detected
            except KeyboardInterrupt as e:
                print("[-] Interrupted")
                sys.exit(0)

            # If successfully cloned, directory should exist
            if pathlib.Path(_cloned_repo_location).exists() == False:
                _unsuccessfully_cloned.append(_package_['name'])
                print(" -> Failed !")

        else:
            # Append package to the exclusion list
            # if package is not git clonable
            _not_git_package.append(_package_['name'])

    # Append package that was not successfully cloned to the list
    if len(_unsuccessfully_cloned) == 0:
        print(f"[+] All repositories cloned")
    else:
        print(f"[!] Repositories that failed to be cloned:")
        for p in _unsuccessfully_cloned:
            print(f"\t- Failed: [ {p} ]")

    # Check if any non-git packages were found
    if len(_not_git_package) == 0:
        print("[*] No non-git package(s) found")
    else:
        print("[!] The following package(s) were excluded:")
        for p in _not_git_package:
            print(f"\t- Excluded: [ {p} ]")

def arg_parser():

    _version_ = "0.4"

    p = argparse.ArgumentParser(prog="MTPR", description="MTPR - Mirror This Pentest Repo package cloner", )
    p.add_argument(
        "-f",
        "--file",
        help="Location of file containing repositories (e.g packages.json)",
        required=False
        )
    p.add_argument(
        "-v",
        "--version",
        help="Version of the script",
        action="store_true",
        required=False
    )

    args = p.parse_args(args=None if sys.argv[1:] else ["-h"])

    if args.version:
        print(f"[*] Script is version  ({_version_})")
        sys.exit(0)

    # Begin
    gitcloner(args.file)

if __name__ == "__main__":
    arg_parser()

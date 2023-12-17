#!/usr/bin/env python3

import os
import sys
import json
import pathlib

try:
    import git # GitPython
except ImportError as e:
    raise Exception(f"[-] Missing required python library - \n {e}")

__version__ = 0.3

# Check if provided argument is a file
def isfile(json_file):

    file = False

    if os.path.isfile(json_file):
        file = True

    return file

# Is the package a git repo to clone ?
def ispackage_git(_json):

    _isgit = False

    '''
    check_isfile = isfile(json_file)
    if check_isfile == False:
        print("[-] Specified argument is not a file")
        sys.exit(-1)

    json_file = pathlib.Path(json_file).resolve()

    with open(json_file, "r") as _package:
        _json = json.load(_package)

        if _json["git"] == True:
            _isgit = True
    '''

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

# Performs the cloning of repos
def gitcloner(json_file):

    print(f"[+] Starting repository cloning - ({json_file})")

    _json = parseJson(json_file)
    _package_ = ""

    _not_git_package = []

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

            # Do cloning of repo
            try:
                _clone = git.Repo.clone_from(_git_url, f"{_git_clone_location}{_git_repo_category}/{_git_repo_name}")
                print(_clone)
                input("PAUSE")
                if _clone:
                    print(f"\t+ [ {_git_repo_name} ] - Clone successful")
            except Exception as e:
                print("- Cloning failed")
                print(e)

        else:
            # Append package to the exclusion list
            # if package is not git clonable
            _not_git_package.append(_package_['name'])

    # Check if any non-git packages were found
    if len(_not_git_package) == 0:
        print("[-] No non-git package(s) found")
    else:
        print("[!] The following package(s) were excluded:")
        for p in _not_git_package:
            print(f"\t- Excluded: [ {p} ]")

if __name__ == "__main__":

    _helpmsg = "[*] Usage: mtpr.py </path/to/package.json>"

    if len(sys.argv) < 2:
        print(_helpmsg)
        sys.exit(1)

    file = sys.argv[1]

    # BEGIN
    gitcloner(file)
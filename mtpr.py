#!/usr/bin/env python3

import os
import sys
import json
import pathlib
import git # GitPython

# __version__ = 0.2

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
        print("Specified argument is not a file")
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
        print("Specified argument is not a file")
        sys.exit(-1)

    # Resolve the file location
    json_file = pathlib.Path(json_file).resolve()

    # open the package file 
    with open(json_file, "r") as _package:
        _json = json.load(_package)

    return _json

# Performs the cloning of repos
def gitcloner(json_file):
    
    _json = parseJson(json_file)
    _package_ = ""
    
    _not_git_package = []

    # Loop through all packages in the package.json file
    for repo in _json:
        _package_ = _json[repo]
    
        # Check if package is clonable (git valid)
        _git_check = ispackage_git(_package_)
        if _git_check == True:
            
            # Set the vars for each attribute of a package
            _git_repo_name = _package_["name"]
            _git_url = _package_["url"]
            _git_clone_location = _package_["location"]

            # Do cloning of repo
            try:
                _clone = git.Repo.clone_from(_git_url, _git_clone_location + _git_repo_name)
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
        print("No non-git package(s) found")
    else:
        print("The following package(s) were excluded:")
        for p in _not_git_package:
            print(f"\t- [ {p} ]")

if __name__ == "__main__":
    
    _helpmsg = "Usage: mtpr.py </path/to/package.json>"

    if len(sys.argv) < 2:
        print(_helpmsg)
        sys.exit(1)

    file = sys.argv[1]

    # BEGIN
    gitcloner(file)

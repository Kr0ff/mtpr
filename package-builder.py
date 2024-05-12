#!/usr/bin/env python3

import argparse
import json
import sys


# Build process of JSON
def build_package(name, url, location, category, git=False):
        # Prepare variables
        _pname      = name
        _purl       = url
        _plocation  = location
        _pgit       = git
        _pcategory  = category


        # JSON structure 
        _json_struct = {
                _pname :{
                        "name"      : _pname,
                        "url"       : _purl,
                        "location"  : _plocation,
                        "git"       : _pgit,
                        "category"  : _pcategory
                        }
                }

        # Create the JSON object with parsed data
        _json = json.dumps(_json_struct, indent=4)

        print(_json)

# Argument parser
def arg_parser():
        p = argparse.ArgumentParser(description="MTPR - JSON Package builder")
        p.add_argument(
                "-n",
                "--name",
                help="Name of package (e.g impacket)",
                required=True
                )
        
        p.add_argument(
                "-u",
                "--url",
                help="URL of where package would be downloaded from",
                required=True
                )
        
        p.add_argument(
                "-l",
                "--location",
                help="Location where to save the package/tool",
                required=True
                )

        p.add_argument(
                "-g",
                "--git",
                action="store_true",
                help="Is package from GitHub/GitLab (True if selected)",
                required=False
                )

        p.add_argument(
                "-c",
                "--category",
                help="Category of tools the repository belongs to (e.g post-ex)",
                choices=[
                        'c2', 
                        'cloud', 
                        'code-audit', 
                        'cracking', 
                        'exploitation', 
                        'malware', 
                        'misc', 
                        'osint', 
                        'persistence', 
                        'phishing', 
                        'post-ex', 
                        'privesc', 
                        'recon', 
                        'vpn', 
                        'web'
                        ],
                
                required=True
                )

        args = p.parse_args(args=None if sys.argv[1:] else ["-h"])

        #------------------------------

        if args.git:
                _pgit = True

        build_package(
                args.name, 
                args.url, 
                args.location, 
                args.category,
                args.git
                )

if __name__ == "__main__":
        arg_parser()

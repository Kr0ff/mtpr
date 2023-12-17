# mtpr
**M**irror **T**his **P**entest **R**epo is a simple tool to grab quickly pentest tools or similar from GitHub/Gitlab.

The project is quite simple and is useful when having to set up quickly a pentest laptop/desktop or a virtual machine. 

While it does not replace a fully fledged pentest dedicated OS such as Kali Linux, Blackarch, ParrotSec OS, Backbox, etc, it allows to quickly download a set of tools, scripts, etc from a number of developers in GitHub or Gitlab.

It is possible to create one JSON file containing many tools that you like to use for your job. 

While the packages have to be created by the user, the main concept is that, you create one package and use it with  mtpr to quickly clone all of the repositories, so you're set and ready to start pentesting or doing a CTF.

> Warning: The tool does not currently download submodules for git repositories. This means if you're cloning a repository that requires some submodules be cloned alongside it to work properly, those won't be cloned. You will have to do it manually.

### Package format

The format of a JSON file is:

```json
{
	"impacket": {                                           # Package name
		"name": "impacket",                             # Repository name
		"url": "https://github.com/fortra/impacket",    # URL of repository
		"location": "/home/$USER/git/",                 # Location for repository to be cloned to 
		"git": true,                                    # Is package from GitHub or GitLab
		"category": "post-ex"				# Category for the repository
	}
}

```

The above JSON format can be created automatically with the `package-builder.py` file. Just provide the arguments and copy/paste the output to the JSON package file you're building.

```sh
./package-builder.py -n impacket -u "https://github.com/fortra/impacket" -l "/home/$USER/git/" -g -c "post-ex"
{
    "impacket": {
        "name": "impacket",
        "url": "https://github.com/fortra/impacket",
        "location": "/home/$USER/git",
        "git": true,
	"category": "post-ex"
    }
}
```
> NOTE: An ending / is required for the folder where the packages will be cloned, otherwise and error will be thrown and repository won't be cloned.

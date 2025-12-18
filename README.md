# monkey business bundler

The monkey business bundler is a simple build and release CLI tool.

It supports the following flags:
- `-d`, `--dirname`, `./` - the directory to bundle.
- `-g`, `--git` - only bundles files tracked by git
- `-v`, `--verbose` - adds verbose logging

mbb supports a `.mbbignore` file which can be written like the following:

```
.git
.venv
build/example.py
# this is a comment and will be skipped
README.md
```

mbb outputs a `.tar.gz` bundle in the executed directory. The title of the bundle is the basename
of the path. If the `-g` flag is used, the git hash and branch will also be included and seperated
by a `-` in the form of `<basename>-<branch>-<hash>`

mbb's functionality is subject to change without any notice. Updates will remain backwards compatible.

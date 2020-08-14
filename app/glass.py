#!/usr/bin/env python
from os.path import dirname, join
from glasskit.commands import main
from ask import app


if __name__ == '__main__':
    cmd_path = join(dirname(__file__), "commands")
    raise SystemExit(main(app))

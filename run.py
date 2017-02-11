#!/usr/bin/python3

import sys
import os.path
pygtklibdir = os.path.join("/usr/lib", "serial2cmd")
sys.path.insert(0, pygtklibdir)
execfile(os.path.join(pygtklibdir, "serial2cmd_ui.py"))

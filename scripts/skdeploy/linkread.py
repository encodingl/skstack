#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from optparse import OptionParser
import sys

def parseOption(argv):
    def _optionsError(errorMsg, callFunc):
        logError("**Error: parserOption Error. %s" % emsg)
        if DEBUG and callFunc: callFunc()
        print(json.dumps({"Status": False, "Command": 'parserOption', 'CommandException': emsg}))
        sys.exit(1)
    parser = OptionParser(version="%prog 1.0.0")
    parser.add_option("-r", "--release-to", dest="releaseto", default=False,
                        help="In which tag/branch need to compile and package this project")
    (options, args) = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return options 

if __name__ == "__main__":
    options = parseOption(sys.argv[1:])
    print(os.readlink(options.releaseto))


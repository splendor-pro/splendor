#! /usr/bin/env python
#coding: utf-8

from common import *
from preparation.create_db_schema import DB_SCHEMA
from preparation.create_cpg import create_cpg
#module 1 anchor api detectors
from model.AnchorDetector import *
#module 2 triple matching
from model.TripleMatcher import *
#module 3 taint track
from model.VulTracker import *


def main(target_dir="", exist_db=False, exist_cpg=False):
    '''
        the entrance of the splendor
    '''
    # preparation 1: data schema building
    print("{C}[!] Step 1: create the database schema...{R}".format(C=C.RED, R=C.RESET))
    db_handler = DB_SCHEMA()
    # pass the target dir to analysis
    if not exist_db:
        db_handler.create_db_schema(target_dir)
        print("{C}[+] db schema create...ok{R}".format(C=C.CYAN, R=C.RESET))
        db_handler.db_analysis()
        print("{C}[+] db schema analysis...ok{R}".format(C=C.CYAN, R=C.RESET))

    # preparation 2 : cpg building
    print ("{C}[!] Step 2: create the cpg...{R}".format(C=C.RED, R=C.RESET))
    #
    if not exist_cpg:
        create_cpg(target_dir)
        print("{C}[+] CPG create... ok{R}".format(C=C.CYAN, R=C.RESET))

    # process: anchor API detector
    AnchorDetector().run()
    # process: fuzzy match
    TripleMatcher().run()
    # process: taint analysis
    VulTracker.taint_analysis()


#
if __name__ == '__main__':
    main("./done", True, True)

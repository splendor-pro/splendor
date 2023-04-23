#coding: utf-8
import time
import json
from collections import *
from cpg.gremlin.gremlin_handler import *

gremlin = gremlinHandler()

class color:
  RED   = "\033[1;31m"
  BLUE  = "\033[1;34m"
  YELLOW = "\033[1;33m"
  CYAN  = "\033[1;36m"
  GREEN = "\033[0;32m"
  RESET = "\033[0;0m"
  BOLD    = "\033[;1m"
  REVERSE = "\033[;7m"
C = color()

_banner = """{red}
 _______  _______  ___      _______  __    _  ______   _______  ______   
|       ||       ||   |    |       ||  |  | ||      | |       ||    _ |  
|  _____||    _  ||   |    |    ___||   |_| ||  _    ||   _   ||   | ||  
| |_____ |   |_| ||   |    |   |___ |       || | |   ||  | |  ||   |_||_ 
|_____  ||    ___||   |___ |    ___||  _    || |_|   ||  |_|  ||    __  |
 _____| ||   |    |       ||   |___ | | |   ||       ||       ||   |  | |
|_______||___|    |_______||_______||_|  |__||______| |_______||___|  |_|v 1.1
{reset}""".format(red=C.CYAN, reset=C.RESET)


print(_banner)


if __name__ == '__main__':
    _ql = "g.V.count()"
    res = gremlin.query(_ql)
    print(res)
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    c1="haha2"
    os.mkdir("/tmp/yyappgw")
    with open("/tmp/yyappgw/1.txt","a+") as f: 
        f.write(c1)
  
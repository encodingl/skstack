#! /usr/bin/env python
# -*- coding: utf-8 -*-

def new_file(file_name,file_content):
    with open(file_name,"a+") as f:
        f.write(file_content)
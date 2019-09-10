#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年6月14日 @author: encodingl
'''

def my_obj_pairs_hook(lst):
    result={}
    count={}
    for key,val in lst:
        if key in count:count[key]=1+count[key]
        else:count[key]=1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key]=[result[key], val]
        else:
            result[key]=val
    return result
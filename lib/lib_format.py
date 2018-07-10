#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年4月10日 @author: skipper
'''

def list_to_formlist(args):

    list_args = args

 
    
    list_tumple = []
    for l in list_args:
        l=str(l)
        t1=(l,l)
        list_tumple.append(t1)
 
        
    return list_tumple

if __name__ == '__main__':
    lt1=[2,1,3]
    fl=list_to_formlist(lt1)
    print fl
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os



def db_record_create(model,**values):
    if retcode==0:
        retcode="success"
    else:
        retcode="failed"

    model.objects.create(**values)
    
def test(x,**y):
    if y==0:
        x="suc"
    else:
        x="fai"
    print x,y
    
if __name__ == '__main__':
    
    test("b",y=0,y1=4,y2=5)
    
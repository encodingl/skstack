#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import redis
if __name__ == "__main__":
    rc = redis.Redis(host='127.0.0.1',password='redis0619')
    ps = rc.pubsub()
    ps.subscribe(['c1', 'c2'])
    rc.publish('c1', 'hello c1')
    rc.publish('c2', 'hello c2')
    rc.publish('c2', 'hello c2')
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from gittle import Gittle

def get_git_tag(repo_path,repo_url):
    repo = Gittle(repo_path,origin_uri=repo_url)
    list_tags = repo.tags.keys()
    list_tumple_tags = []
    for l in list_tags:
        t1=(l,l)
        list_tumple_tags.append(t1)
        
    return list_tumple_tags
    
if __name__ == "__main__":
    repo_url="git@gitlab.szyy.com:szgroup/yy-app-gw.git"
    repo_path="/opt/data/gitsource/prod/yyappgw"
    
    l=get_git_tag(repo_path,repo_url)
    print l
    





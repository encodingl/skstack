#! /usr/bin/env python
# -*- coding: utf-8 -*-

from gittle import Gittle

from git  import *
import re

def get_git_tag(repo_path,repo_url):
    repo = Gittle(repo_path,origin_uri=repo_url)
    list_tags = repo.tags.keys()
 
    list_tags = sorted(list_tags,reverse=True)
    list_tumple_tags = []
    for l in list_tags:
        t1=(l,l)
        list_tumple_tags.append(t1)
        
    return list_tumple_tags

def get_git_commitid(repo_path):
    g = Repo(repo_path,odbt=GitDB)
    list_commitid = list(g.iter_commits("master", max_count=10))
 
   
    list_tumple_commitid = []
    for l in list_commitid:
        l = str(l)
        t1=(l,l)
        list_tumple_commitid.append(t1)
        
    return list_tumple_commitid
    
if __name__ == "__main__":
    repo_url="git@gitlab.szyy.com:opergroup/skipper.git"
    repo_path="/opt/data/gitsource/prod/skipper"
    
    Repo.clone_from(url=repo_url, to_path="/tmp/cl4/")
    
    
#     g = Repo(repo_path,odbt=GitDB)
#     list_commitid = list(g.iter_commits("master", max_count=15))
#     print type(list_commitid)
#     l=[]
#     p = r'"(.*)"'
#     for i in list_commitid:
#         print i
#         print type(i)
#         i = str(i)
#         print type(i)
#         l.append(i)
# #         i = str(i)
# #         i = re.search(p,i)
# #         ig = i.group()
# #         l.append(ig)
#     print l
    
    
    

    





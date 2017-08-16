#! /usr/bin/env python
# -*- coding: utf-8 -*-

from gittle import Gittle


def get_git_tag(repo_path,repo_url):
    repo = Gittle(repo_path,origin_uri=repo_url)
    list_tags = repo.tags.keys()
 
    list_tags = sorted(list_tags,reverse=True)
    list_tumple_tags = []
    for l in list_tags:
        t1=(l,l)
        list_tumple_tags.append(t1)
        
    return list_tumple_tags
    
if __name__ == "__main__":
    repo_url="git@gitlab.szyy.com:opergroup/skipper.git"
    repo_path="/opt/data/gitsource/prod/skipper"
    repo = Gittle(repo_path, origin_uri=repo_url)
    print repo.active_branch
    repo.checkout("v0.1.0.000")
    print repo.active_branch

    
    

    





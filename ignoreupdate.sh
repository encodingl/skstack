#!/bin/bash
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
./gitpush.sh update.gitignore

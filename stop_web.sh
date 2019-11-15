#!/bin/bash
ps -ef|grep skstack|grep -v grep|awk '{print $2}'|xargs kill

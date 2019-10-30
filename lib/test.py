#! /usr/bin/env python
# -*- coding: utf-8 -*-



if __name__ == "__main__":
    s1 = "{u'main_task': ('inner_var:\\u6211\\u662fzw\nmultiple_vars:a1\nmultiple_vars:a2\nsingle_var:6\n', None), u'post_task': ('inner_var:\\u6211\\u662fzw\nmultiple_vars:a1\nmultiple_vars:a2\nsingle_var:6\n', None)}"
    print(s1.decode("unicode_escape"))
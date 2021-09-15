# coding: utf-8
def highlight(s):
    return "%s[32;1m%s%s[0m" % (chr(27), s, chr(27))
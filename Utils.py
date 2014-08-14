# coding=utf-8
import os

def is_markdown(fpath):
    return os.path.isfile(fpath) and fpath[-3:] == '.md'

def stripext(fpath):
    return fpath[:fpath.rindex('.')]

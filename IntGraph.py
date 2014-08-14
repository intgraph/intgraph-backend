# coding=utf-8
import os
import sys

import gData
import Config
from View import ListView, FlatView

import logging

def main():
    (gData.indir, gData.outdir) = (sys.argv[1], sys.argv[2])
    
    views = []
    
    for item in os.listdir(gData.indir):
        path = os.path.join(gData.indir, item)
        if os.path.isdir(path) and not item.startswith('.'):
            views.append(ListView(item))
        elif item.endswith('.md'):
            views.append(FlatView(item))
    
    map(lambda x: x.generate(), views)

if __name__ == '__main__':
    main()

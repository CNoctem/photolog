import glob
import logging
import os
import sys

import time
from datetime import datetime

import mylogger
import pactions
import pfilters
from pfile import PFile

log = mylogger.getLogger(level = logging.DEBUG)

class Argparser:
    actions = []
    filters = []

    def __init__(self):
        args = sys.argv[1:]
        for i, a in enumerate(sys.argv[1:]):
            if a == 'from':
                self.startDate = args[i + 1]
            elif a == 'to':
                self.endDate = args[i + 1]
            elif os.path.isdir(a):
                self.root = args[i]
            elif a == 'put':
                self.actions.append(pactions.PutAction())
            elif a == 'filter':
                self.filters.append(pfilters.FilenameFilter(args[i + 1]))
                self.extensions = args[i + 1].split(',')
            # elif a == 'get':



        self.postInit()

    def postInit(self):
        if hasattr(self, 'startDate'):
            if not hasattr(self, 'endDate'):
                self.endDate = datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S')
            self.filters.append(pfilters.DateFilter(self.startDate, self.endDate))


def collect(argparser):
    c = []
    log.info('Collecting')
    t0 = time.time()
    for file in glob.iglob(argparser.root + '/**/*', recursive=True):
        for e in argparser.extensions:
            if file.endswith('.' + e):
                c.append(PFile(file))
    log.info('Collected %s files in %ss' % (len(c), time.time() - t0))
    return c


def allApply(file, filters):
    for f in filters:
        if not f.apply(file):
            return False
    return True


def filter(collection, filters):
    filtered = []
    for file in collection:
        if allApply(file, filters):
            filtered.append(file)
    return filtered


ap = Argparser()
log.info('Root:\t\t\t\t%s' % ap.root)

all = collect(ap)
for p in all:
    for f in ap.filters:
        if f.apply(p):
            for a in ap.actions:
                a.act(p)

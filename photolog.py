import glob
import logging
import os
import sys

import time
from datetime import datetime

import mylogger
import pactions
import pcollectors
import pfilters
from pfile import PFile

log = mylogger.getLogger(level = logging.DEBUG)

class Argparser:
    collectors = []
    actions = []
    filters = []

    def __init__(self):
        self.collection = []
        args = sys.argv[1:]
        for i, a in enumerate(sys.argv[1:]):
            if a == 'from':
                self.startDate = args[i + 1]
            elif a == 'to':
                self.endDate = args[i + 1]
            elif os.path.isdir(a):
                self.root = args[i]
            elif a == 'put':
                self.actions.append(pactions.PutAction(self))
            elif a == 'filter':
                self.filters.append(pfilters.FilenameFilter(args[i + 1]))
                self.extensions = args[i + 1].split(',')
            elif a == 'get':
                pass

        self.postInit()

    def postInit(self):
        if hasattr(self, 'startDate'):
            if not hasattr(self, 'endDate'):
                self.endDate = datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S')
            self.filters.append(pfilters.DateFilter(self.startDate, self.endDate))
        self.collectors.append(pcollectors.FileCollector(self))


    def collect(self):
        for c in ap.collectors:
            self.collection += c.collect()

    def runfinlters(self):
        coll = []
        self.collect()
        for c in self.collection:
            if self.allfiltersapply(c):
                coll.append(c)
        self.collection = coll

    def allfiltersapply(self, pfile):
        for f in self.filters:
            if not f.apply(pfile):
                return False
        return True



ap = Argparser()
log.info('Root:\t\t\t\t%s' % ap.root)

ap.runfinlters()
print(ap.collection)

for f in ap.collection:
    for a in ap.actions:
        a.act(f)

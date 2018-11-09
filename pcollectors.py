import glob
import logging

import time

import mylogger
import pfile


class Collector:

    def __init__(self, argparser):
        self.ap = argparser

    def collect(self):
        pass


class FileCollector(Collector):

    log = mylogger.getLogger(name='filecollector', level=logging.DEBUG)

    def collect(self):
        c = []
        self.log.info('Collecting')
        t0 = time.time()
        for file in glob.iglob(self.ap.root + '/**/*', recursive=True):
            for e in self.ap.extensions:
                if file.endswith('.' + e):
                    c.append(pfile.PFile(file))
        self.log.info('Collected %s files in %ss' % (len(c), time.time() - t0))
        return c

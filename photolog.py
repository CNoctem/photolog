import glob
import sys, os
import time

import exifread
from datetime import datetime

TAG_DATETIME_ORIG = 'EXIF DateTimeOriginal'


class PFile:
    def __init__(self, filename):
        self.filename = filename
        f = open(self.filename, 'rb')
        t0 = time.time()
        self.tags = exifread.process_file(f)
        dt = time.time() - t0
        print('TAGS ', filename, ' in ', dt)

    def getTag(self, tagname):
        return self.tags[tagname]


class Filter:
    def apply(self, pFile):
        return True


class DateFilter(Filter):
    def __init__(self, startDateStr, endDateStr):
        self.start = parseDate(startDateStr)
        self.end = parseDate(endDateStr)

    def apply(self, pfile):
        dto = str(pfile.getTag(TAG_DATETIME_ORIG))
        t = parseDate(dto)
        return self.start <= t <= self.end


class Argparser:
    dateFilterOn = False

    def __init__(self):
        args = sys.argv[1:]
        for i, a in enumerate(sys.argv[1:]):
            if a == 'from':
                self.startDate = args[i + 1]
            elif a == 'to':
                self.endDate = args[i + 1]
            elif os.path.isdir(a):
                self.root = args[i]
        self.postInit()

    def postInit(self):
        if hasattr(self, 'startDate'):
            if not hasattr(self, 'endDate'):
                self.endDate = datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S')
            self.dateFilterOn = True


def parseDate(dateStr):
    try:
        return datetime.strptime(dateStr, '%Y:%m:%d')
    except:
        return datetime.strptime(dateStr, '%Y:%m:%d %H:%M:%S')


def collect(root, extensions):
    c = []
    print('Collecting')
    t0 = time.time()
    for file in glob.iglob(root + '/**/*', recursive=True):
        for e in extensions:
            if file.endswith('.' + e):
                c.append(PFile(file))
    print('Collected', len(c), 'files in', time.time() - t0, 's')
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


filters = []
ap = Argparser()
print('Root:\t\t\t\t', ap.root)

all = collect(ap.root, ['JPG'])
if ap.dateFilterOn:
    print('Date filter [ON]:\t', ap.startDate, '...', ap.endDate)
    filters.append(DateFilter(ap.startDate, ap.endDate))
else:
    print('Date filter [OFF]')

print("Filtering...")
for f in filter(all, filters):
    print(f.filename, ' .. ', f.getTag(TAG_DATETIME_ORIG))

# print(isDateOrigBetween(tags, ap.startDate, ap.endDate))

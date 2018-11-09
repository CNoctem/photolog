import exif_const
from util import parseDate

class Filter:
    def apply(self, pfile):
        return True


class DateFilter(Filter):
    def __init__(self, startDateStr, endDateStr):
        self.start = parseDate(startDateStr)
        self.end = parseDate(endDateStr)

    def apply(self, pfile):
        dto = str(pfile.getTag(exif_const.TAG_DATETIME_ORIG))
        t = parseDate(dto)
        return self.start <= t <= self.end

class FilenameFilter(Filter):
    def __init__(self, extensionlist):
        self.extensions = extensionlist.split(',')

    def apply(self, pfile):
        for e in self.extensions:
            if pfile.filename.endswith(e):
                return True
        return False

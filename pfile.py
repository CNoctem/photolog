import time
import exifread


class PFile:
    def __init__(self, filename):
        self.filename = filename

    def getTag(self, tagname):
        if not hasattr(self, 'tags'):
            t0 = time.time()
            f = open(self.filename, 'rb')
            self.tags = exifread.process_file(f)
            dt = time.time() - t0
            print('TAGS ', self.filename, ' in ', dt)
        return self.tags[tagname]

    def __str__(self):
        return '<pfile name=' + self.filename + '>'

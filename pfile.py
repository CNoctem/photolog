import time
import exifread


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

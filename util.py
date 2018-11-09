from datetime import datetime

def parseDate(dateStr):
    try:
        return datetime.strptime(dateStr, '%Y:%m:%d')
    except:
        return datetime.strptime(dateStr, '%Y:%m:%d %H:%M:%S')

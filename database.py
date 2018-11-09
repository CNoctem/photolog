import logging

import sqlite3

import exif_const
import mylogger

log = mylogger.getLogger(name = 'DB', level = logging.DEBUG)

def createColListForTable():
    list = ''
    for t in exif_const.tags:
        list += ',' + t.replace(' ', '_') + " STRING"
    return list

def createColListForValues():
    list = ''
    for t in exif_const.tags:
        list += ',' + t.replace(' ', '_')
    return list

def createValuesList(pfile):
    list = ''
    for t in exif_const.tags:
        list += ',"' + str(pfile.getTag(t)) + '"'
    return list

class PDB:

    SQL_CREATE_EXIF_DATA    =  'CREATE TABLE IF NOT EXISTS EXIF_DATA (' +\
                                'ID INTEGER PRIMARY KEY AUTOINCREMENT,' +\
                                'FILENAME STRING%s)'


    SQL_INSERT_PFILE        =   'INSERT INTO EXIF_DATA ' +\
                                '(FILENAME%s) ' +\
                                'VALUES (%s)'

    SQL_SELECT_PFILE        =   'SELECT FILENAME FROM EXIF_DATA WHERE FILENAME = "%s"'


    def __init__(self, dbfile):
        self.openDB(dbfile)
        self.connection = self.openDB(dbfile)

        self.SQL_CREATE_EXIF_DATA = self.SQL_CREATE_EXIF_DATA % createColListForTable()
        self.SQL_INSERT_PFILE = self.SQL_INSERT_PFILE % (createColListForValues(),'"%s"%s')

        self.execute(self.SQL_CREATE_EXIF_DATA)

    def openDB(self, dbfile):
        conn = sqlite3.connect(dbfile)
        return conn

    def execute(self, q):
        log.info('executing query \'%s\'.' % q)
        cursor = self.connection.execute(q)
        self.connection.commit()
        return cursor


    def put_if_not_exists(self, pfile):
        log.info('checking file %s.' % pfile.filename)
        filename = pfile.filename
        rows = self.execute(self.SQL_SELECT_PFILE % filename).fetchall()


        if len(rows) != 0:
            log.info('RowCount = %s.' % len(rows))
            log.info('File %s is already stored.' % filename)
        else:
            log.info('putting file %s.' % pfile.filename)
            self.execute(self.SQL_INSERT_PFILE % (pfile.filename, createValuesList(pfile)))

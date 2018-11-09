import os

import database

directory = os.getenv("HOME") + '/.photolog'
if not os.path.exists(directory):
    os.makedirs(directory)

db = database.PDB(directory + '/photolog.db')


class Action:

    def __init__(self, argparser):
        self.ap = argparser

    def act(self, pfile):
        pass

class PutAction(Action):

    def act(self, pfile):
        db.put_if_not_exists(pfile)

class GetAction(Action):

    def act(self, pfile):
        





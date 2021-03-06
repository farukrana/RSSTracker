#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Dec 23, 2012

@author: J Carroll
@emaill: jrcarroll@jrcresearch.net
'''

import sqlite3 as sq
from datetime import datetime

__DB_NAME__ = 'FeedDB.db'
__DB_TABLE__ = 'feeds'


class CreateFeedDB():
    def __init__(self, DBname=__DB_NAME__, DBtable=__DB_TABLE__):
        """
        Connects to the database and adds a table as necessary
        """
        self.__db__ = DBname
        # connect to the database
        self.db = sq.connect(self.__db__)
        # this is the feed table - it has all the info we need about feeds!
        self.table = DBtable
        # the cursor object - we use this to communicate to the DB
        self.cursor = self.db.cursor()
        
        self.create_table(self.table)
        
        self.URL = None
        
    def create_table(self, table):
        """
        Attempts to create the main feeds table - if it does not exists, it will
        make it
        """

        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 
                           __DB_TABLE__ + 
                           "(id INTEGER PRIMARY KEY, URIType TEXT DEFAULT RSS, URL TEXT, Active INTEGER DEFAULT 0, Added TEXT, Last_Checked TEXT DEFAULT 'Never Checked')")
        except:
            raise

    def execute_general(self, commands):
        self.cursor.execute(commands)
        self.db.commit()
        
        
class ConnectFeedDB():
    def __init__(self, DBname=__DB_NAME__, DBtable=__DB_TABLE__):
        """
        Connects to the database and adds a table as necessary
        """

        self.db = DBname
        self.db = sq.connect(self.db)
        self.table = DBtable
        self.cursor = self.db.cursor()
        self.selected_feed = None
        self.pragma_table = self.cursor.execute("PRAGMA TABLE_INFO(feeds)")
        self.pragma_split()
        self.all_feeds = []
    
    def pragma_split(self):
        """
        Creates a list of the pragma information + column names
        """
        
        self.__temp__ = []
        for i in self.pragma_table:
            self.__temp__.append(i)
        self.pragma_table = self.__temp__
        del self.__temp__

    def select_feed(self, by, value):
        self.selected_feed = self.cursor.execute("SELECT * FROM {0} WHERE {1} = {2}".format(self.table,
                                                                                            by,
                                                                                            value))
        return self.selected_feed.fetchall()
    
    def add_feed(self, URIType, URL):
        """Add a feed"""
        
        self.__sql_add__ = "INSERT INTO feeds (URIType, URL, Active, Added) \
        VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\")".format(URIType, URL, 1, datetime.ctime(datetime.now()))
        self.cursor.execute(self.__sql_add__)
        self.db.commit()
        
    def activate_feed(self, URL):
        """Activate feeds"""
        self.__sql_update__ = "UPDATE feeds SET Active = 1 WHERE id = \"{0}\" AND Active = 0".format(URL)
        self.cursor.execute(self.__sql_update__)
        self.db.commit()
            
    def deactivate_feed(self, id):
        """Deactivate an active feed"""
        self.__sql_update__ = "UPDATE feeds SET Active = 0 WHERE id = \"{0}\" AND Active = 1".format(id)
        print self.__sql_update__
        self.cursor.execute(self.__sql_update__)
        self.db.commit()
    
    def return_all_feeds(self):
        """Return a generator object that contains all the feed detail"""
        all_feeds = self.cursor.execute("SELECT * from feeds")
        self.all_feeds = []
        for feed in all_feeds:
            self.__temp__ = {}
            for i in range(0, len(feed), 1):
                self.__temp__[self.pragma_table[i][1]] = feed[i]
            self.all_feeds.append(self.__temp__)
        return self.all_feeds

    def del_feedBY(self, column, value):
        
        sql_del = "DELETE FROM {0} WHERE {1} = {2}".format(self.table, column, value)
        self.cursor.execute(sql_del)
        self.db.commit()

    def del_all_feeds(self):
        sql_all = "DELETE FROM {0}".format(self.table)
        self.cursor.execute(sql_all)
        self.db.commit()
    
    def check_feed(self, id):
        sql_check = "UPDATE feeds SET Last_Checked = \"{0}\" WHERE id = {1}".format(datetime.ctime(datetime.now()), id)
        
        self.cursor.execute(sql_check)
        self.db.commit()
        self.return_all_feeds()

if __name__ == '__main__':
    v = ConnectFeedDB()
    v.add_feed("RSS", "alj.com")
    v.add_feed("RSS", "13423fj.com")
    v.add_feed("RSS", "alkea231.com")
    v.add_feed("RSS", "ae23.com")
    v.add_feed("RSS", "a91991j.com")
    v.add_feed("RSS", "google.com")
    print v.return_all_feeds()
    
    pass

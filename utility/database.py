import sqlite3
from sqlite3 import Error
import datetime
import os
from os import path
import json
from cryptography.fernet import Fernet
############### DATABSE SECTION ##################
# Class that help to use and connect to database #
# Configuration into config.json                 #
##################################################
class DB:
    def getDbName() -> str:
        config_file = open("config.json")
        configuration = json.load(config_file)

        db = configuration['database_path'] + configuration['database_name'] 

        return db

    def getDbConnection() -> object:
        db = DB.getDbName()
        try:
            connection = sqlite3.connect(db)
        except Error as e:
            print(e)

        return connection
    def existDB() -> bool:
        db = DB.getDbName()

        if path.exists(db):
            return True
        else:
            return False





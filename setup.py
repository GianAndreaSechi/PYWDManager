import sqlite3
from sqlite3 import Error
from utility.database import DB
import os
from os import path
import json
from cryptography.fernet import Fernet

def createDatabase() -> bool:
    if not DB.existDB():
        try:
            con = DB.getDbConnection()

            cur = con.cursor()
            # Create table
            cur.execute('''
                CREATE TABLE pywd_credentials(
                    service_name text NOT NULL,
                    email text NOT NULL,
                    username text NOT NULL,
                    password text NOT NULL,
                    secret_question text,
                    secret_answer text, 
                    last_update datetime,
                    PRIMARY KEY(service_name, email, username)
                );''')
            con.close()
            

            #creating Fernet Key
            key = Fernet.generate_key()
            
            #saving in file
            config_file = open("config.json")
            configuration = json.load(config_file)
            with open(configuration['key_path'], 'wb') as file_object:  file_object.write(key)

            return True
        except Error as e:
            print(e)
            return False
    else:
        return False

if __name__ == "__main__":
    if DB.existDB():
        print("A DB file is already present!")
    else:
        res = createDatabase()

        if res:
            print("Database created successfully!")
        else:
            print("An error occured!")

    
    
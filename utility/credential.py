from utility.database import DB
import sqlite3
from sqlite3 import Error
import datetime
import os
from os import path
import json
from cryptography.fernet import Fernet
################## CREDENTIAL SECTION ####################
# Class define the credential object and their functions #
##########################################################
class Credential:
    def __init__(self):
        self.service_name = ""
        self.email = ""
        self.username = ""
        self.password = ""
        self.secret_question = ""
        self.secret_answer = ""
        self.last_update = datetime.datetime.now()
    
    def insertCredential(self):
        ##########################################################
        # Allow to insert new credential into database           #
        ##########################################################
        if DB.existDB():
            try:
                con = DB.getDbConnection()

                cur = con.cursor()

                cur.execute('''
                    INSERT INTO pywd_credentials(
                        service_name,
                        email,
                        username,
                        password,
                        secret_question,
                        secret_answer, 
                        last_update
                    )
                    VALUES (?,?,?,?,?,?,?);
                    ''', [self.service_name, self.email, self.username, self.password, self.secret_question, self.secret_answer, self.last_update])
                
                #commit need to validate the query excecution
                con.commit()
                con.close()

                print("Done!")
            except Error as e:
                print(e)
        else:
            print("Database not found!")
    def updateCredential(self):
        ##########################################################
        # Allow to update a specific credential into database    #
        ##########################################################
        if DB.existDB():
            try:
                con = DB.getDbConnection()

                cur = con.cursor()

                cur.execute('''
                    UPDATE pywd_credentials 
                    SET
                        password = ?,
                        last_update = ?
                    WHERE service_name = ? and email = ?;
                    ''', [self.password, self.last_update, self.service_name, self.email])
                
                #commit need to validate the query excecution
                con.commit()
                con.close()

                print("Done!")
            except Error as e:
                print(e)
        else:
            print("Database not found!")
    def cryptPwd(self):
        ##########################################################
        # Crypt the password inserted into database with Fernet  #
        # Need the Key.Bin generated with setup to granted       #
        # consinstency of the password and data                  #
        ##########################################################

        #get the key from the file
        key = Credential.getKey()

        #creating the correct hash from Fernet and encrypt the password
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(self.password.encode())

        self.password = ciphered_text


    def decryptPwd(self) -> str:
        ###########################################################
        # Decrypt the password inserted into database with Fernet #
        # Need the Key.Bin generated with setup to granted        #
        # consinstency of the password and data                   #
        ###########################################################

        #get the key from a file
        key = Credential.getKey()
        
        #creating the correct hash from Fernet and decrypt the password
        cipher_suite = Fernet(key)
        ciphered_text = self.password

        unchifered_password = cipher_suite.decrypt(ciphered_text)

        return unchifered_password.decode() #return the decoded string

    
    def getKey() -> str:
        #get correct path from configuration file
        config_file = open("config.json")
        configuration = json.load(config_file)

        #retrieving the secret key from file
        with open(configuration['key_path'], 'rb') as file_object:
            for line in file_object:
                key = line

        return key
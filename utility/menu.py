from utility.database import DB
from utility.credential import Credential
import sqlite3
from sqlite3 import Error
import datetime
import os
from os import path
import json
from cryptography.fernet import Fernet
########## MENU & FUNCTIONALITY SECTION ##########
# This class initialize and define the user menu #
##################################################
class Menu:
    #menu options to show to the users
    menu_options = {
        1: 'Show all credentials',
        2: 'Search credential',
        3: 'Insert new credential',
        4: 'Update credential',
        5: 'Delete credential',
        6: 'Clear view',
        7: 'Exit',
    }
    def insert():
        ##############################################################
        # This function allow to insert new credential into database #
        ##############################################################
        n_credential = Credential()

        n_credential.service_name = input("Insert service name: ")
        n_credential.email = input("Insert email: ")
        n_credential.username = input("Insert username: ")
        #if input("Do you want to generate your password? Y/n ") == "Y":
        #    generated_pwd = "123456"
        #    n_credential.password = generated_pwd
        #    print("Password generated: ", generated_pwd)
        #else:
        n_credential.password = input("Insert password: ")
    
        n_credential.secret_question = input("Insert service question: ")
        n_credential.secret_answer = input("Insert secret answer: ")
        
        n_credential.cryptPwd()
        n_credential.insertCredential()

    def search():
        ##############################################################
        # This function allow to search a credential by:             #
        # - Service name                                             #
        # - Email                                                    # 
        ##############################################################
        c_service_search = input("What service do you wanna search: ")
        c_email_search = input(f"What email of {c_service_search} do you wanna search: ")

        if DB.existDB():
            try:
                con = DB.getDbConnection()
                con.row_factory = sqlite3.Row #used to have the row as a dictionary format

                cur = con.cursor()

                rows = cur.execute('''SELECT * FROM pywd_credentials WHERE service_name = ? and email = ?''',[c_service_search,c_email_search]).fetchall()
                for row in rows:
                    a_credential = Credential()
                    
                    a_credential.service_name = row['service_name']
                    a_credential.email = row['email']
                    a_credential.username = row['username']
                    a_credential.password = row['password']
                    a_credential.secret_question = row['secret_question']
                    a_credential.secret_answer = row['secret_answer']
                    a_credential.last_update = row['last_update']

                    plain_password = a_credential.decryptPwd()
                    
                    print('| Service | Email | Username | Password | Secret Question | Secret Answer | Last Update |')
                    print("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(row['service_name'],row['email'],row['username'], plain_password,row['secret_question'],row['secret_answer'],row['last_update']))
                    
                #commit need to validate the query excecution
                con.close()
            except Error as e:
                print(e)
        else:
            print("Database not found!")
    def update():
        ##############################################################
        # This function allow to update a credential in databse      #
        ##############################################################
        c_service_search = input("What service do you wanna search: ")
        c_email_search = input(f"What email of {c_service_search} do you wanna search: ")

        if DB.existDB():
            try:
                con = DB.getDbConnection()
                con.row_factory = sqlite3.Row #used to have the row as a dictionary format

                cur = con.cursor()

                rows = cur.execute('''SELECT * FROM pywd_credentials WHERE service_name = ? and email = ?''',[c_service_search,c_email_search]).fetchall()
                for row in rows:
                    a_credential = Credential()
                    
                    a_credential.service_name = row['service_name']
                    a_credential.email = row['email']
                    a_credential.username = row['username']
                    a_credential.password = row['password']
                    a_credential.secret_question = row['secret_question']
                    a_credential.secret_answer = row['secret_answer']
                    a_credential.last_update = row['last_update']

                    plain_password = a_credential.decryptPwd()
                    
                    print('| Service | Email | Username | Password | Secret Question | Secret Answer | Last Update |')
                    print("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(row['service_name'],row['email'],row['username'], plain_password,row['secret_question'],row['secret_answer'],row['last_update']))
                    
                #commit need to validate the query excecution
                #if input("Do you want to generate your password? Y/n ") == "Y":
                #    generated_pwd = "123456"
                #    a_credential.password = generated_pwd
                #    print("Password generated: ", generated_pwd)
                #else:
                a_credential.password = input("Insert new password: ")
                a_credential.last_update = datetime.datetime.now()
                
                a_credential.cryptPwd()

                a_credential.updateCredential()
        
                con.close()
            except Error as e:
                print(e)
        else:
            print("Database not found!")
    def show_all():
        ##############################################################
        # Show all credential in database in plain text              #
        # (only if key file is found)                                #
        ##############################################################
        if DB.existDB():
            try:
                con = DB.getDbConnection()
                con.row_factory = sqlite3.Row #used to have the row as a dictionary format

                cur = con.cursor()

                rows = cur.execute('''SELECT * FROM pywd_credentials''').fetchall()

                print('| Service | Email | Username | Password | Secret Question | Secret Answer | Last Update |')
                for row in rows:
                    a_credential = Credential()
                    
                    a_credential.service_name = row['service_name']
                    a_credential.email = row['email']
                    a_credential.username = row['username']
                    a_credential.password = row['password']
                    a_credential.secret_question = row['secret_question']
                    a_credential.secret_answer = row['secret_answer']
                    a_credential.last_update = row['last_update']

                    plain_password = a_credential.decryptPwd()

                    print("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(row['service_name'],row['email'],row['username'],plain_password,row['secret_question'],row['secret_answer'],row['last_update']))
                    print("-------------------------------------------")
                #commit need to validate the query excecution
                con.close()
            except Error as e:
                print(e)
        else:
            print("Database not found!")

    def delete():
        ##############################################################
        # This function allow to delete a specific a credential      #
        ##############################################################
        c_service_delete = input("What service do you wanna delete: ")
        c_email_delete = input(f"What email of {c_service_delete} do you wanna delete: ")

        if DB.existDB():
            try:
                con = DB.getDbConnection()

                cur = con.cursor()

                cur.execute('''DELETE FROM pywd_credentials WHERE service_name = ? and email = ?''',[c_service_delete,c_email_delete])
                
                #commit need to validate the query excecution
                con.commit()
                con.close()
            except Error as e:
                print(e)
        else:
            print("Database not found!")
    
    def clear():
        ##############################################################
        # Clear the CLI interface                                    #
        ##############################################################
        os.system('cls||clear')

    def print_menu():
        ##############################################################
        # Showing the menu option and handle the user choice         #
        ##############################################################
        options = Menu.menu_options
        print("=================== MENU ===================")
        for key in options.keys():
            print (key, '--', options[key] )
        print("============================================")
    
    def init():
        while(True):
            Menu.print_menu()
            try:
                option = int(input('Enter your choice: '))
            except:
                print('Incorrect input. Please insert a number...')

            #Check what choice was entered and act accordingly
            if option == 1:
                Menu.show_all()
            elif option == 2:
                Menu.search()
            elif option == 3:
                Menu.insert()
            elif option == 4:
                Menu.update()
            elif option == 5:
                Menu.delete()
            elif option == 6:
                Menu.clear()
            elif option == 7:
                print('Thanks message before exiting')
                exit()
            else:
                print('Invalid option. Please enter a number between 1 and 4.')

            #Menu.clear()
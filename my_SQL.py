from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import json
import sqlite3
import instances
DBName="finaldatabase.sqlite"


state_dict = instances.build_state_url_dict()

def build_state_table():
    try:
        connection = sqlite3.connect(DBName)
        
        cursor = connection.cursor()
        cursor.execute(f'''CREATE TABLE States
        (
        Statename varchar(255),
        Stateurl varchar(255)
        )

        ''')
        connection.commit()
        connection.close()
        
        connection = sqlite3.connect(DBName)
        for items in state_dict.items():
            connection = sqlite3.connect(DBName)
            cursor = connection.cursor()
            cursor.execute(f'''INSERT INTO States
            (Statename,Stateurl) 
            VALUES(
            '{items[0]}','{items[1]}'
            )

            ''')
            connection.commit()
            connection.close()
    except:
        pass

def drop_state_table():
    try:
        connection = sqlite3.connect(DBName)
        cursor = connection.cursor()
        cursor.execute(f'''DROP TABLE States
        ''')
        connection.commit()
        connection.close()
    except:
        pass



def build_college_table():
    try:
        connection = sqlite3.connect(DBName)
        cursor = connection.cursor()
        cursor.execute(f'''CREATE TABLE Colleges
        (
        Rank varchar(255),
        Name varchar(255),
        Address varchar(255),
        Zipcode varchar(255),
        Phone varchar(255),
        Tuition_in varchar(255),
        Tuition_out varchar(255),
        Url varchar(255),
        Enrollment varchar(255),
        State varchar(255)
        )

        ''')
        connection.commit()
        connection.close()
    except:
        pass

def insert_college(statename):
    try:
        collegeinstances = instances.get_sites_for_state(state_dict[statename])
        for items in collegeinstances:
            connection = sqlite3.connect(DBName)
            cursor = connection.cursor()
            cursor.execute(f'''INSERT INTO Colleges
            (Rank,Name,Address,Zipcode,Phone,Tuition_in,Tuition_out,Url,Enrollment,State) 
            VALUES(
            '{items.rank}','{items.name}','{items.city}','{items.zipcode}','{items.phone}','{items.tuition_in}','{items.tuition_out}','{items.url}','{items.enrollment}','{statename}'
            )

            ''')
            connection.commit()
            connection.close()
    except:
        pass


def drop_college_table():
    try:
        connection = sqlite3.connect(DBName)
        cursor = connection.cursor()
        cursor.execute(f'''DROP TABLE Colleges
        ''')
        connection.commit()
        connection.close()
    except:
        pass


drop_college_table()

# build_college_table()
# insert_college('arizona')
# insert_college('new york')


drop_state_table()

# build_state_table()
#This file contains all the database helper functions
from typing import Any
import psycopg2
import sys
import configparser

def connect_to_database() -> Any :
    ''' 
        Function to establish the connection to the database
        Arguments : None
        Returns : the connection object to the database
    '''
    cred_file = "./config.cfg"
    
    db_config = configparser.ConfigParser()
    db_config.read(cred_file)
    
    try:
        conn = psycopg2.connect(
            host=db_config['DATABASE']['DB_HOST'],
            port=db_config['DATABASE']['DB_PORT'],
            database=db_config['DATABASE']['DB_NAME'],
            user=db_config['DATABASE']['DB_USER'],
            password=db_config['DATABASE']['DB_PASSWORD'],
        )

        conn.set_session(autocommit=True)
        return conn

    except Exception as e:
        print("Encountered an error in connecting to the database : ", e)
        sys.exit()
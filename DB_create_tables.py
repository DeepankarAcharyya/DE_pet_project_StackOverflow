#Script for connecting to the database and creating the required tables
import os

from DB_utility_funcs import connect_to_database
from DB_SQL_Queries import CREATE_TAG_RAW_TABLE, CREATE_QUESTIONS_RAW_TABLE, CREATE_ANSWERS_RAW_TABLE

#QUERY Execution
try:
    print("Starting the process for creating the required tables...")
    with connect_to_database() as conn :
        cur = conn.cursor()
        cur.execute(CREATE_TAG_RAW_TABLE)
        cur.execute(CREATE_ANSWERS_RAW_TABLE)
        cur.execute(CREATE_QUESTIONS_RAW_TABLE)
    print("Tables created.")

except Exception as e:
    print("Exception encountered while creating the tables : ",e)
    os.exit(1)
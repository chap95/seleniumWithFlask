import sqlite3
from sqlite3.dbapi2 import connect
from db.db_config import *

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

connection.execute('CREATE TABLE if not exists ' + TABLE_NAME + ' (' +
                   'ID TEXT PRIMARY KEY NOT NULL, '
                   'DESCRIPTION TEXT NOT NULL, ' + ' );')

connection.commit()
connection.close()

import sqlite3
from flask import g

DATABASE_DIRETION = "/"
DB_NAME = "result.db"
TABLE_NAME = 'ResultTable'
DATABASE_PATH = DATABASE_DIRETION + '/' + DB_NAME


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.row

    return g.db

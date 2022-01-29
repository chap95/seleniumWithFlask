import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE_DIRETION = "/db"
DB_NAME = "result.db"
TABLE_NAME = 'ResultTable'
DATABASE_PATH = DATABASE_DIRETION + '/' + DB_NAME


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    print("close db")
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    print("init db")
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    print("init app")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

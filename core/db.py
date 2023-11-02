import sqlite3

from core.storage import db_path
from core.tables import create_table

con = sqlite3.connect(db_path)
cur = con.cursor()

create_table(con)

def getCon() -> sqlite3.Connection:
    return con


def getCur() -> sqlite3.Cursor:
    return cur

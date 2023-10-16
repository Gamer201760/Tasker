import sqlite3

from core.tables import create_table

con = sqlite3.connect('./tasker.db')
cur = con.cursor()

create_table(con)

def getCon() -> sqlite3.Connection:
    return con


def getCur() -> sqlite3.Cursor:
    return cur

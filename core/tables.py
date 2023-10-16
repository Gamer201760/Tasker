import sqlite3

TABLES = """
create table if not exists User (
    id uuid,
    username string,
    token string,
    ejusername string,
    primary key(id)
);
create table if not exists Task (
    id uuid,
    text string,
    user_id uuid,
    deadline date,
    state bool,
    FOREIGN KEY (user_id) REFERENCES User (id)
);
"""


def create_table(con: sqlite3.Connection):
    con.executescript(TABLES)
    con.commit()

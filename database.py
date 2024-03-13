import sqlite3
con = sqlite3.connect("mydb.db")
cur = con.cursor()
cur.execute('Create Table ToDo(id integer primary key Autoincrement,Title TEXT,Description TEXT,Images TEXT)')
# cur.execute("alter table ToDo add photo TEXT")
con.commit()
con.close()
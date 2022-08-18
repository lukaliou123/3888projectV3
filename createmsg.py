import sqlite3

conn = sqlite3.connect("database.db")

# conn.execute("drop table message")

conn.execute("CREATE TABLE message (\n"
    "\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "\ttext TEXT NOT NULL,\n"
    "\tsender INTEGER NOT NULL,\n"
    "\treceiver INTEGER NOT NULL,\n"
    "\ttime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
    "\tFOREIGN KEY(receiver) REFERENCES Users(user_id),\n"
    "\tFOREIGN KEY(sender) REFERENCES Users(user_id)\n);"
)

# test
# conn.execute("INSERT INTO messages values(1,'hello',2,1,'2021-04-04 11:24:54');")
# conn.execute("INSERT INTO messages values(2,'hi',1,2,'2021-04-04 11:35:54');")
# conn.execute("INSERT INTO messages values(3,'Can I have your number?',2,1,'2021-04-04 11:36:54');")

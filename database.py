import sqlite3

conn = sqlite3.connect('Data.db')
c = conn.cursor()

class DataBase:
    def __init__(self, token, username):
        self.token = token
        self.username = username
    
    @classmethod
    def GetFromDB(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return c.fetchall()

    def GoToDB(self):
        with conn:
            c.execute(f"INSERT INTO 'main'.'Users'('id','token','username') VALUES (NULL, ?, ?)",(self.token, self.username))
    
    @classmethod
    def Count(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return len(c.fetchall())
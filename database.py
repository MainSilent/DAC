import pycurl
import sqlite3

conn = sqlite3.connect('Data.db')
c = conn.cursor()

class DataBase:
    def __init__(self,username,uID,send):
        self.username = username
        self.uID = uID
        self.send = send
    
    @classmethod
    def GetFromDB(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return c.fetchall()

    def GoToDB(self):
        with conn:
            c.execute(f"INSERT INTO 'main'.'Users'('ID','username') VALUES (NULL,?)",(self.username,))
    
    @classmethod
    def Count(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return len(c.fetchall())
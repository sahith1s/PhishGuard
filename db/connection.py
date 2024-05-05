import sqlite3 as sq
class Connection:
    conn = sq.connect("phishing.db", check_same_thread=False)
    cursor = conn.cursor()
    users_table = "users"

    def execute(self, query):
        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            print(row)
            return row
        except Exception as e:
            return None
    def executeAll(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            return rows
        except Exception as e:
            return None

    def commit(self):
        self.conn.commit()

    def create(self, fields):
        try:
            if fields==3:
                query = f"create table phishing_users_db (uname TEXT  PRIMARY KEY,email TEXT,pwd TEXT);"
                self.cursor.execute(query)
        except Exception as e:
            print(e)
        try:
            if fields==2:
                query = "create table phishingDataBase (url TEXT PRIMARY KEY, status TEXT);"
                self.cursor.execute(query)
        except Exception as e:
            print(e)
       



    def insert(self, *fields):
        print(fields)
    
        if len(fields) == 4:
            query = f"insert into {fields[0]} values('{fields[1]}','{fields[2]}','{fields[3]}')"
        elif len(fields) == 3:
            query = f"insert into {fields[0]} values('{fields[1]}','{fields[2]}')"
     


        print(query)
        try:
            a = self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            return None
        return a

import pymysql

class DBHandler:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user = user
        self.password=password
        self.database=database

    def login(self,email,password):
        mydb = None
        mydbCursor=None
        inserted = False
        ex=None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "select * from user where email=%s and password=%s"
            args = (email,password)
            mydbCursor.execute(sql, args)
            row=mydbCursor.fetchone()
            if row:
                inserted=True
        except Exception as e:
            ex=e
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            if inserted:
                return True
            else:
                return ex
            
    def signUp(self,data):
        mydb = None
        mydbCursor=None
        inserted = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from user where email=%s"
            args1=(data[1])
            mydbCursor.execute(sql1, args1)
            results = mydbCursor.fetchone()
            if results ==None:
                sql1="insert into user (name,email,password) values (%s,%s,%s)"
                args1=(data[0],data[1],data[2])
                mydbCursor.execute(sql1, args1)
                mydb.commit()
                inserted=True
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
    
            return  inserted


    def getid(self,u):
        mydb = None
        mydbCursor=None
        results=None
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            args=(u,)
            sql = "select userid from users where email=%s"
            mydbCursor.execute(sql,args)
            results=mydbCursor.fetchall()
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return results
    
    #Enter Notes name in DB
    def enterNoteName(self,email,noteName):
        mydb = None
        mydbCursor=None
        id=None
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            args=(email,)
            sql = "select id from user where email=%s"
            mydbCursor.execute(sql,args)
            id=mydbCursor.fetchall()
            if(id):
                args=(id,noteName,)
                sql1="insert into notes  (userid,notename) values (%s,%s)"
                mydbCursor.execute(sql1, args)
                mydb.commit()
                inserted=True
        except Exception as e:
            print(e)
        finally:
                if mydbCursor != None:
                    mydbCursor.close()

                if mydb != None:
                    mydb.close()
        
                return  inserted


    def get_note_names_for_user(self, email):
        mydb = None
        mydbCursor = None
        note_names = []
        
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()

            # Fetch user ID by email
            args = (email,)
            sql = "SELECT id FROM user WHERE email=%s"
            mydbCursor.execute(sql, args)
            user_id = mydbCursor.fetchone()

            if user_id:
                user_id = user_id[0]  # Extracting the user ID from the tuple
                args = (user_id,)
                sql = "SELECT notename FROM notes WHERE userid=%s"
                mydbCursor.execute(sql, args)
                note_names = [row[0] for row in mydbCursor.fetchall()]
            
        except Exception as e:
            print(e)
        finally:
            if mydbCursor:
                mydbCursor.close()
            if mydb:
                mydb.close()

            return note_names

    def delete_all_notes_for_user(self,email):
        mydb = None
        mydbCursor = None

        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()

            # Fetch user ID by email
            args = (email,)
            sql = "SELECT id FROM user WHERE email=%s"
            mydbCursor.execute(sql, args)
            user_id = mydbCursor.fetchone()

            if user_id:
                user_id = user_id[0]  # Extracting the user ID from the tuple
                args = (user_id,)
                sql = "DELETE FROM notes WHERE userid=%s"
                mydbCursor.execute(sql, args)
                mydb.commit()
                return True  # Deletion successful

        except Exception as e:
            print(e)
            return False  # Deletion failed

        finally:
            if mydbCursor:
                mydbCursor.close()
            if mydb:
                mydb.close()

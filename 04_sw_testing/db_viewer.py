import sqlite3
import os


class Singleton:
    count = 0
    cursor = None
    db_name = 'aquarium.db' 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
            cls.instance.get_cursor()
        return cls.instance

    def __init__(self):
        self.count += 1

    def get_cursor(self):
        if os.path.exists("aquarium.db"):
            print("DB found, getting cursor")
            self.connection = sqlite3.connect("aquarium.db")
            self.cursor = self.connection.cursor()
        else:
            print("DB NOT found!  run initialize_database first")
            self.cursor = None
            

    def sql(self, sql_statement):
        if self.cursor:
            print("Executing: {}".format(sql_statement))
            try:
                rows = self.cursor.execute(sql_statement).fetchall()
            except Exception as e:
                print(e)
                return []
            return rows
        else:
            print("No database connection")
            return []


def initialize_database(): 
    """Initialise a file, and use sqlite3 to generate a small table we'll use for testing"""
    connection = sqlite3.connect("aquarium.db")
    cursor = connection.cursor()
    print("INTIALIZING DATABASE")
    cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
    cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
    cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
    connection.commit()

def delete_database():
    """Delete, or clear the entire database completely
       Sqlite3 uses files to store your date, so clearing it just deleting the file
    """
    if os.path.exists('aquarium.db'):
        os.remove('aquarium.db')
   
def db_fresh_start():
    """For testing purposes, it's useful to reset to a known state.
        So we clear the database, and then unitialize it with only our small set of data
    """
    delete_database()
    initialize_database()

################################
# ***** TESTS *****
################################
def test_is_singleton():
    delete_database()
    a = Singleton()
    b = Singleton()
    assert id(a) == id(b)
    
def test_not_initialized():
    delete_database()
    db = Singleton()
    assert [] == db.sql("SELECT * FROM FISH;")

def test_database_connect():
    db_fresh_start()
    db = Singleton()
    db.get_cursor()
    assert 2 == len(db.sql("SELECT * FROM fish;"))

def test_resetting_after_db_creation():
    delete_database()

    db_a = Singleton()
    db_b = Singleton()
    assert id(db_a) == id(db_b)
    db_a.get_cursor()
    assert [] == db_a.sql("SELECT * FROM FISH;")
    assert [] == db_b.sql("SELECT * FROM FISH;")

    initialize_database()

    db_a.get_cursor()
    assert 2 == len(db_b.sql("SELECT * FROM fish;"))


    
if __name__=="__main__":

    
    db = Singleton()
    
    while True:
        stmt = input("=> ")
        if stmt == 'quit':
            break

        rows = db.sql(stmt)
        for row in rows:
            print(row)
            


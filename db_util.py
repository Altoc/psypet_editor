import sqlite3

# Function to connect to the SQLite database
def connect_to_database():
    conn = sqlite3.connect('D:\psypet_prototype\psypet\data\database.db')
    return conn
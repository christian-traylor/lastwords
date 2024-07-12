import sqlite3

def initialize_db(db_name='people.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inmates (
        id INTEGER PRIMARY KEY,
        last_statement TEXT,
        name TEXT,
        date_of_birth TEXT,
        education_level TEXT,
        age_at_offense INTEGER,
        race TEXT,
        gender TEXT,
        date_executed TEXT
    );
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
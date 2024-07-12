import sqlite3
import pandas as pd
import json

DATABASE_NAME = 'people.db'
DATA_SOURCE_FILE = 'data.json'
TABLE_NAME = 'inmates'

def extract_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        normalized_data = []
        for inmate_id, details in data.items():
            inmate_info = details['inmate_information']
            normalized_record = {
                'id': inmate_id,
                'last_statement': details['last_statement'],
                'date_executed': details['date_executed']
            }
            normalized_record.update(inmate_info)
            normalized_data.append(normalized_record)
        df = pd.DataFrame(normalized_data)
        return df
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error during data extraction: {e}")
        return None

def transform_data(df):
    try:
        # df = df.dropna()
        
        df = df.rename(columns={
            'id': 'id',
            'last_statement': 'last_statement',
            'Name': 'name',
            'Date of Birth': 'date_of_birth',
            'Education Level (Highest Grade Completed)': 'education_level',
            'Age (at the time of Offense)': 'age_at_offense',
            'Race': 'race',
            'Gender': 'gender',
            'date_executed': 'date_executed'
        })

        active_columns = {
            'id', 
            'last_statement', 
            'name',
            'date_of_birth',
            'education_level',
            'age_at_offense',
            'race',
            'gender',
            'date_executed'
        }

        for column in df.columns:
            if column not in active_columns:
                df.drop(column, axis=1, inplace=True)

        df.columns = [col.strip().lower() for col in df.columns]

        return df
    except Exception as e:
        print(f"Error during data transformation: {e}")
        return None

def load_data(df, db_name, table_name):
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        print(f"Data loaded successfully into {table_name}")
    except sqlite3.Error as e:
        print(f"Error during data loading: {e}")

def main():
    data = extract_data(DATA_SOURCE_FILE)
    print(data)
    if data is not None:
        transformed_data = transform_data(data)
        print(transformed_data)
        if transformed_data is not None:
            load_data(transformed_data, DATABASE_NAME, TABLE_NAME)

# Execution
if __name__ == '__main__':
    main()
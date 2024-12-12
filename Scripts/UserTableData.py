import pandas as pd
import mysql.connector 
import random

data = pd.read_csv('/Users/lohithreddyporeddy/Desktop/Projects/SQL/LibraryDB/MOCK_DATA_USERS.csv')
print(data.head())

print(data.columns.tolist())

data['JoinDate'] = pd.to_datetime(data['JoinDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')


DB_PARAMS = {
    'host':'localhost',
    'user':'your_username',
    'password':'your_password',
    'database':'LibraryDB'
}

required_columns = ['User_ID', 'Name', 'Email', 'PhoneNumber', 'JoinDate', 'Role']

missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    raise ValueError(f"Missing required columns{missing_columns}")

try:
    conn = mysql.connector.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for _,row in data.iterrows():
        try:
            cursor.execute('''
            INSERT INTO Users (Name, Role, Email, PhoneNumber, JoinDate)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Name = VALUES(Name),
                Role = VALUES(Role),
                Email = VALUES(Email),
                JoinDate = VALUES(JoinDate),
                PhoneNumber = VALUES(PhoneNumber);
            ''', (
                row['Name'], 
                row['Role'], 
                row['Email'], 
                row['PhoneNumber'],
                row['JoinDate']
            ))
        except Exception as e:
            print(f"Error inserting row: {e}")
    conn.commit()
    print("Data loaded successfully 👍")
except mysql.connector.errors as e:
    print(f"Failed to connect :{e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()

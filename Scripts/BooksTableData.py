import pandas as pd
data = pd.read_csv('/Users/lohithreddyporeddy/Desktop/Projects/SQL/LibraryDB/books.csv')
print("The columns in the dataset are:")
print(data.columns.tolist())

#Code to load the tables in library dataset with the downloaded csv file.
import random
import mysql.connector

DB_PARAMS = {
    'host':'localhost',
    'user':'your_username',
    'password':'your_password',
    'database':'LibraryDB'
}

required_columns = ['title','authors','categories','isbn13','published_year']
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    raise ValueError(f"missing equired columns: {missing_columns}")

filtered_data = data[required_columns].copy()
filtered_data['published_year'] = pd.to_numeric(filtered_data['published_year'], errors='coerce')
filtered_data['published_year'] = filtered_data['published_year'].fillna(0)  # or another default year

filtered_data = filtered_data.dropna()

filtered_data = filtered_data.rename(columns={'authors': 'Author','title':'Title','categories':'Genre','isbn13':'ISBN','published_year':'PublishedYear'})
filtered_data['TotalCopies'] =  10
filtered_data['AvailableCopies']= [random.randint(1,10) for _ in range(len(filtered_data))]

try:
    conn = mysql.connector.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for _, row in filtered_data.iterrows():
        try:
            cursor.execute('''
            INSERT INTO Books (Title, Author, Genre, ISBN, PublishedYear, TotalCopies, AvailableCopies)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Title = VALUES(Title),
                Author = VALUES(Author),
                Genre = VALUES(Genre),
                PublishedYear = VALUES(PublishedYear),
                TotalCopies = VALUES(TotalCopies),
                AvailableCopies = VALUES(AvailableCopies);
            ''', (row['Title'], row['Author'], row['Genre'], row['ISBN'], row['PublishedYear'], row['TotalCopies'], row['AvailableCopies']))
        except Exception as e:
            print(f"Error inserting row: {e}")
    conn.commit()
    print("Data loaded successfully 👍")
except mysql.connector.errors as e:
    print(f"failed to connect to MYSQL: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()



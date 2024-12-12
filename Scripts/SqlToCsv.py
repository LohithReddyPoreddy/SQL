import mysql.connector
import csv

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="your_usename",
    password="your_password",
    database="LibraryDB"
)

cursor = conn.cursor()

# List of tables to export
tables = ["Books", "Users", "BorrowedBooks", "LateFee"]

for table in tables:
    # Query to fetch all rows
    query = f"SELECT * FROM {table}"
    cursor.execute(query)

    # Fetch column names
    columns = [desc[0] for desc in cursor.description]

    # File name for the CSV
    filename = f"{table}.csv"

    # Writing to CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(columns)

        # Write data rows
        writer.writerows(cursor.fetchall())

    print(f"Data from {table} exported to {filename}")

# Close connections
cursor.close()
conn.close()

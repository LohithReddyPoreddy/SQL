import mysql.connector
DB_PARAMS = {
    'host':'localhost',
    'user':'your_username',
    'password':'your_password',
    'database':'LibraryDB'
}

late_fee_per_day = 2
try:
    conn = mysql.connector.connect(**DB_PARAMS)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""select BorrowID, UserID, DueDate, ReturnDate 
                   from BorrowedBooks
                   where ReturnDate is not null
                   """)
    
    borrowed_books = cursor.fetchall()

    for record in borrowed_books:
        borrow_id = record['BorrowID']
        user_id = record['UserID']
        due_date = record['DueDate']
        return_date = record['ReturnDate']

        if return_date > due_date:
            late_days = (return_date-due_date).days
            late_fee = late_days*late_fee_per_day
        else:
            late_days=0
            late_fee=0
        if late_fee > 0:
            cursor.execute(""" insert into LateFee(UserID, BorrowID, Amount) 
                        values (%s, %s, %s)""", (user_id, borrow_id, late_fee))
        
    conn.commit()
    print("Late fees populated successfully 👍")

except mysql.connector.errors as e:
    print(f"Error connecting to MYSQL : {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()

import pandas as pd
import random
import mysql.connector
from datetime import datetime, timedelta


class BorrowedBooksData:
    def __init__(self,host,user,password,database):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'your_username',
            password = 'your_password',
            database = 'LibraryDB'
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def get_book_with_available_copies(self):
        query = """ SELECT BookID, TotalCopies - AvailableCopies as BorrowedCopies
        From Books
        where TotalCopies>AvailableCopies"""

        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_active_users(self):
        query = """SELECT UserID from Users where Role = 'Member'"""
        self.cursor.execute(query)
        return [row['UserID'] for row in self.cursor.fetchall()]
    
    def generate_borrow_records(self):
        borrowed_books = self.get_book_with_available_copies()
        active_users = self.get_active_users()

        total_records = sum(book['BorrowedCopies'] for book in borrowed_books)
        borrow_records =[]

        for book in borrowed_books:
            book_id = book['BookID']
            copies_to_borrow = book['BorrowedCopies']

            for _ in range(copies_to_borrow):
                user_id = random.choice(active_users)
                borrow_date = datetime.now() - timedelta(days = random.randint(0,365))
                due_date = borrow_date + timedelta(days= random.choice([14,30]))
                is_returned = random.random() > 0.3
                return_date = (borrow_date + timedelta(days=random.randint(7,35))) if is_returned else None

                borrow_records.append({
                    'UserID' : user_id,
                    'BookID' : book_id,
                    'BorrowDate': borrow_date,
                    'DueDate':due_date,
                    'ReturnDate': return_date
                })
        return borrow_records
    
    def populate_table(self):
        try:
            borrow_records = self.generate_borrow_records()
            query = """INSERT INTO BorrowedBooks
            (UserID, BookID, BorrowDate, DueDate, ReturnDate)
            VALUES(%s, %s, %s, %s, %s)"""

            records_to_insert = [
                (
                    record['UserID'],
                    record['BookID'],
                    record['BorrowDate'],
                    record['DueDate'],
                    record['ReturnDate']) for record in borrow_records
                
            ]
            self.cursor.executemany(query, records_to_insert)
            self.connection.commit()

            print(f"Successfully inserted {self.cursor.rowcount} records into borrowed books table")
        except mysql.connector.Error as e:
            self.connection.rollback()
            print(f"Error :{e}")
        
        finally:
            self.cursor.close()
            self.connection.close()
def main():
    populator = BorrowedBooksData(
        host = 'localhost',
        user = 'root',
        password = 'Lohith@9381',
        database = 'LibraryDB'
    )

    populator.populate_table()

if __name__ == '__main__':
    main()


    
    



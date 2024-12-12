create database LibraryDB;

use LibraryDB;

-- The tables needed for this project are
-- 1. Users
-- 2. Books
-- 3. Borrowed Books
-- 4. Late Fee

#Creating Users table with reuired columns
create table Users(
	UserID int auto_increment primary key,
    `Name` varchar(100),
    `Role` Enum('Member','Staff') not null,
    Email varchar(100) unique,
    PhoneNumber varchar(15),
    `JoinDate` date
);

#Creating Books table with required columns
create table Books(
	BookID int auto_increment primary key,
    Title varchar(200),
    Author varchar(100),
    Genre varchar(50),
    ISBN varchar(20) unique,
    PublishedYear year,
    TotalCopies int not null,
    AvailableCopies int not null
);

#Creating Borrowed Books table with required columns
create table BorrowedBooks(
	BorrowID int auto_increment primary key,
    UserID int,
    BookID int,
    BorrowDate date,
    DueDate date,
    ReturnDate date,
    foreign key (UserID) references Users(UserID),
    foreign key (BookID) references Books(BookID)
);

#Creating Late Fee table with required columns
create table LateFee(
	FeeID int auto_increment primary key,
    UserID int,
    BorrowID int,
    Amount decimal(10,2),
    foreign key (UserID) references Users(UserID),
    foreign key (BorrowID) references BorrowedBooks(BorrowID)
)


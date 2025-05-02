# SBank CLI Banking App

## Description

This is a CLI-based banking application built using Python and MySQL. It allows users to manage banking accounts, including checking balances, making deposits, and withdrawing funds. The app connects to a MySQL database to store user data and transactions.

## Prerequisites

Before running the application, ensure that you have the following installed on your machine:

- [Python](https://www.python.org/downloads/) (version 3.x or later)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
  - MySQL Workbench is used to manage the MySQL database, create tables, and view your data.

## Setup Instructions

### Step 1: Install Python Dependencies

1. Clone or download the repository to your local machine.
2. Install the necessary Python libraries by running the following command:

   ```bash
   pip install mysql-connector-python

### -- Create Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00
);

-- Create Transactions Table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

###
def connect_db():
    db_config = {
        'host': '',  # <== Replace with your MySQL server host (e.g., 'localhost' or IP address)
        'user': '',  # <== Replace with your MySQL username (e.g., 'root')
        'password': '',  # <== Replace with your MySQL password
        'database': '',  # <== Replace with the name of your database
        'port':  # <== Replace with the MySQL port if different from 3306
    }



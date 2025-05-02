import mysql.connector

def connect_db():
    db_config = {
        'host': '',  # Replace with your MySQL server host (e.g., 'localhost' or IP address)
        'user': '',  # Replace with your MySQL username (e.g., 'root')
        'password': '',  # Replace with your MySQL password
        'database': '',  # Replace with the name of your database
        'port': 3306  # Replace with the MySQL port if different from 3306
    }

    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


# Make sure to add this SQL code in MySQL Workbench or your MySQL environment to create the necessary tables.

# Create Users Table
# CREATE TABLE users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     balance DECIMAL(10, 2) DEFAULT 0.00
# );

# Create Transactions Table
# CREATE TABLE transactions (
#     transaction_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     transaction_type VARCHAR(50) NOT NULL,
#     amount DECIMAL(10, 2) NOT NULL,
#     transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );

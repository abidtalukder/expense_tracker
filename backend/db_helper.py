from contextlib import contextmanager
import mysql.connector
from datetime import datetime, date
from setup_logger import get_logger

logger = get_logger("db_helper", "db_helper.log")

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')  # Adjust the format to match your date strings
        return True
    except ValueError:
        return False

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123.",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connected to MySQL database")
    else:
        raise Exception("Failed to connect to MySQL database")

    cursor = connection.cursor(dictionary=True)

    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()
    print("MySQL connection is closed")

# fetching functions
def fetch_expenses_for_date(date):
    logger.info(f"Fetching expenses for date: {date}")

    if not is_valid_date(date):
        return []

    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (date,))
        expenses = cursor.fetchall()
        return expenses

def fetch_expenses_by_date_range(start_date, end_date):
    logger.info(f"Fetching expenses between {start_date} and {end_date}")

    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date BETWEEN %s AND %s", (start_date, end_date))
        return cursor.fetchall()

def fetch_expenses_by_category(category):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE category=%s", (category,))
        return cursor.fetchall()

def delete_expense(expense_id):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))

def add_expense(date,amount,category,notes):
    logger.info(f"Adding expense: {date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s, %s, %s, %s)", (date,amount,category,notes))

def delete_expenses_by_date(date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date=%s", (date,))

## Analysis functions
def helper_expense_to_category_percent(expenses):
    category_expenses = {}
    sum = 0
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        sum += amount
        if category in category_expenses:
            category_expenses[category] += amount
        else:
            category_expenses[category] = amount

    for category in category_expenses:
        category_expenses[category] = round((category_expenses[category] / sum) * 100,2)

    return category_expenses

def break_expense_by_category_percentage(start_date, end_date):
    expenses = fetch_expenses_by_date_range(start_date, end_date)
    return helper_expense_to_category_percent(expenses)

def fetch_expense_summary(start_date, end_date):
    logger.info(f"Fetching expense summary between {start_date} and {end_date}")

    # if not is_valid_date(start_date) or not is_valid_date(end_date):
    #     return []

    with get_db_cursor() as cursor:
        cursor.execute("SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY category", (start_date, end_date))
        return cursor.fetchall()

if __name__ == "__main__":
    print("db_helper.py")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    print(summary)
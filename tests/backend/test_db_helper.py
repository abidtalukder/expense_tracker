from backend import db_helper

def test_fetch_expenses_for_date():
    date = "2024-08-15"
    expenses = db_helper.fetch_expenses_for_date(date)
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 10
    assert expenses[0]["category"] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"

def test_fetch_expenses_invalid_date():
    date = "9999"
    expenses = db_helper.fetch_expenses_for_date(date)
    assert len(expenses) == 0

def test_fetch_summary_invalid():
    start_date = "9999"
    end_date = "20000"
    summary = db_helper.fetch_expense_summary(start_date, end_date)
    assert len(summary) == 0

def test_fetch_summary():
    start_date = "2024-08-01"
    end_date = "2024-08-05"
    summary = db_helper.fetch_expense_summary(start_date, end_date)
    assert len(summary) == 5
    assert summary[0]["category"] == "Entertainment"
    assert summary[0]["total"] == 225
    assert summary[1]["category"] == "Shopping"
    assert summary[1]["total"] == 670

if __name__ == '__main__':
    print("test_db_helper.py")

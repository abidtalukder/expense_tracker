from fastapi import FastAPI
from fastapi import Body
from datetime import date
from typing import List

import db_helper
from datatypes import Expense

app = FastAPI()

#TODO: validate date format
@app.get("/expenses/{day}", response_model=List[Expense])
def get_expenses(day):
    return db_helper.fetch_expenses_for_date(day)

@app.post("/expenses/{expense_date}")  # Correct path with leading slash
def add_or_update_expense(expense_date, expenses:List[Expense]=Body(...)):
    db_helper.delete_expenses_by_date(expense_date)
    for expense in expenses:
        db_helper.add_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"status": "success"}


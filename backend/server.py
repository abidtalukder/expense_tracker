from fastapi import FastAPI
from fastapi import Body
from datetime import date
from typing import List

import db_helper
from datatypes import *

import setup_logger
app = FastAPI()

logger = setup_logger.get_logger("server", "server.log")

#TODO: validate date format
@app.get("/expenses/{day}", response_model=List[Expense])
def get_expenses(day):
    logger.info(f"Fetching expenses for date: {day}")
    return db_helper.fetch_expenses_for_date(day)

@app.post("/expenses/{expense_date}")  # Correct path with leading slash
def add_or_update_expense(expense_date, expenses:List[Expense]=Body(...)):
    logger.info(f"Adding or updating expenses for date: {expense_date}")
    db_helper.delete_expenses_by_date(expense_date)
    for expense in expenses:
        db_helper.add_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"status": "success"}

@app.post("/analytics")
def get_analytics(date_range: DateRange = Body(...)):
    logger.info(f"Fetching analytics between {date_range.start_date} and {date_range.end_date}")

    totals = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    total = sum([total["total"] for total in totals])

    breakdown = {}
    for item in totals:
        percentage = round((item["total"] / total) * 100, 2) if total > 0 else 0
        breakdown[item["category"]] = {"total": item["total"], "percentage": percentage}

    return breakdown


from datetime import date
from pydantic import BaseModel
from typing import Optional

class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    notes: str
    expense_date: Optional[date] = None
    category: str
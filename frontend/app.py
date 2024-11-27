import streamlit as st
from datetime import datetime
import requests
import matplotlib.pyplot as plt

# Title of the app
st.title("Expense Tracker")

# tabs
add_tab, analytics_tab = st.tabs(["Add Expenses", "Analytics"])

API_URL = "http://localhost:8000"

with add_tab:
    expense_date = st.date_input("Date", datetime(2024,8,1), label_visibility="collapsed")

    # get expense details for date
    response = requests.get(f"{API_URL}/expenses/{expense_date}")
    expenses = []
    if response.status_code == 200:
        expenses = response.json()
    else:
        st.error("Failed to fetch expenses")

    # create form that fills in the expense details
    categories = ["Shopping", "Rent", "Food", "Entertainment","Other"]

    with st.form("expense_details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            col1.subheader("Amount")

        with col2:
            col2.subheader("Category")

        with col3:
            col3.subheader("Notes")

        expenses_form = []

        for i in range(5):

            col1, col2, col3 = st.columns(3)

            if i < len(expenses):
                amount = expenses[i]["amount"]
                category = expenses[i]["category"]
                notes = expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                amount_input = st.number_input(label="Amount", value=amount, step=0.01,key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, label_visibility="collapsed", key=f"notes_{i}")

            if amount_input > 0:
                expenses_form.append({"amount": amount_input, "category": category_input, "notes": notes_input})

        submit_button = st.form_submit_button("Submit")



        if submit_button:
            response = requests.post(f"{API_URL}/expenses/{expense_date}", json=expenses_form)
            if response.status_code == 200:
                st.success("Expenses added successfully")
            else:
                st.error("Failed to add expenses")

with analytics_tab:
    start_date = st.date_input("Start Date", datetime(2024,8,1), label_visibility="collapsed")
    end_date = st.date_input("End Date", datetime(2024,8,1), label_visibility="collapsed")

    response = requests.post(f"{API_URL}/analytics", json={"start_date": start_date.isoformat(), "end_date": end_date.isoformat()})
    analytics = {}
    if response.status_code == 200:
        analytics = response.json()
    else:
        st.error("Failed to fetch analytics")

    # display analytics with a pie chart
    labels = list(analytics.keys())
    values = [analytics[label]["percentage"] for label in labels]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')

    # display the chart
    st.pyplot(fig)





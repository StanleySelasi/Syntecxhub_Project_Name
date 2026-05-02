import sqlite3
import argparse
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()
    
def add_transaction(t_type, amount, category, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO transactions (type, amount, category, description, date)
    VALUES (?, ?, ?, ?, ?)
    """, (t_type, amount, category, description, date))

    conn.commit()
    conn.close()

    print("✅ Transaction added successfully!")
    
def get_summary(month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, SUM(amount) FROM transactions
    WHERE strftime('%Y-%m', date) = ?
    GROUP BY type
    """, (month,))

    results = cursor.fetchall()
    conn.close()

    income = 0
    expense = 0

    for r in results:
        if r[0] == "income":
            income = r[1]
        elif r[0] == "expense":
            expense = r[1]

    balance = income - expense

    print(f"\n📊 Summary for {month}")
    print(f"Income: {income}")
    print(f"Expenses: {expense}")
    print(f"Balance: {balance}")
    
def category_breakdown(month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount) FROM transactions
    WHERE type='expense' AND strftime('%Y-%m', date)=?
    GROUP BY category
    """, (month,))

    results = cursor.fetchall()
    conn.close()

    print("\n📂 Category Breakdown:")
    for cat, amt in results:
        print(f"{cat}: {amt}")

    return results

def export_csv(filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Amount", "Category", "Description", "Date"])
        writer.writerows(rows)

    conn.close()

    print(f"📁 Exported to {filename}")

def generate_chart(month):
    data = category_breakdown(month)

    if not data:
        print("No data for chart.")
        return

    categories = [x[0] for x in data]
    amounts = [x[1] for x in data]

    plt.figure()
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title(f"Expenses Breakdown - {month}")

    filename = f"chart_{month}.png"
    plt.savefig(filename)

    print(f"📈 Chart saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Advanced Expense Tracker CLI")

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("type", choices=["income", "expense"])
    add_parser.add_argument("amount", type=float)
    add_parser.add_argument("category")
    add_parser.add_argument("description")

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("month")
    
    breakdown_parser = subparsers.add_parser("breakdown")
    breakdown_parser.add_argument("month")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("filename")

    chart_parser = subparsers.add_parser("chart")
    chart_parser.add_argument("month")

    args = parser.parse_args()

    init_db()

    if args.command == "add":
        add_transaction(args.type, args.amount, args.category, args.description)

    elif args.command == "summary":
        get_summary(args.month)

    elif args.command == "breakdown":
        category_breakdown(args.month)

    elif args.command == "export":
        export_csv(args.filename)

    elif args.command == "chart":
        generate_chart(args.month)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
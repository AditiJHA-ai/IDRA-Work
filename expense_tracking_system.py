import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"


def initialize_csv():
    """Ensure the CSV file exists with the proper column headers."""
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount", "Note"])
        except IOError as e:
            print(f"Error initializing CSV file: {e}")


def get_valid_date():
    """Prompt for a valid date in YYYY-MM-DD format or default to today's date."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    while True:
        user_input = input(
            f"Enter date (YYYY-MM-DD) [Default: {today_str}]: "
        ).strip()
        if not user_input:
            return today_str
        try:
            valid_date = datetime.strptime(user_input, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")


def get_valid_amount():
    """Prompt for a positive numeric amount with exception handling."""
    while True:
        try:
            amount = float(input("Enter amount spent: ").strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Invalid input! Please enter a valid numerical value.")


def add_expense():
    """Add a new expense record and append it to the CSV file."""
    print("\nAdd New Expense")

    date_val = get_valid_date()

    category = input("Enter category (e.g., Food, Transport, Rent): ").strip()
    while not category:
        print("Category field cannot be blank.")
        category = input("Enter category: ").strip()

    amount = get_valid_amount()
    note = input("Enter an optional note: ").strip()

    try:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [date_val, category.capitalize(), f"{amount:.2f}", note]
            )
        print("Expense record saved successfully.")
    except IOError as e:
        print(f"Failed to write to file: {e}")


def read_all_expenses():
    """Read and return all expense rows as a list of dictionaries."""
    expenses = []
    if not os.path.exists(CSV_FILE):
        return expenses

    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["Amount"] = float(row["Amount"])
                    expenses.append(row)
                except (ValueError, KeyError):
                    continue
    except IOError as e:
        print(f"Error reading file: {e}")

    return expenses


def view_all_expenses():
    """Display all recorded expenses and the total accumulated expenditure."""
    print("\nAll Recorded Expenses")
    expenses = read_all_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Note'}")

    total_spent = 0.0
    for exp in expenses:
        total_spent += exp["Amount"]
        print(
            f"{exp['Date']:<12} | {exp['Category']:<15} | {exp['Amount']:<10.2f} | {exp['Note']}"
        )

    print(f"\nTotal Amount Spent: {total_spent:.2f}")


def view_category_summary():
    """Aggregate total expenditure per category with percentage breakdown."""
    print("\nCategory-wise Spending Summary")
    expenses = read_all_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}
    total_spent = 0.0

    for exp in expenses:
        cat = exp["Category"]
        amt = exp["Amount"]
        summary[cat] = summary.get(cat, 0.0) + amt
        total_spent += amt

    print(f"{'Category':<20} | {'Total Amount':<12} | {'Percentage'}")

    for cat, total in summary.items():
        percentage = (total / total_spent * 100) if total_spent > 0 else 0.0
        print(f"{cat:<20} | {total:<12.2f} | {percentage:.1f}%")

    print(f"\nOverall Total: {total_spent:.2f}")


def main():
    """Main application loop."""
    initialize_csv()

    while True:
        print("\nEXPENSE TRACKING SYSTEM")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Category-wise Summary")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            view_category_summary()
        elif choice == "4":
            print("\nExiting Expense Tracking System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()

"""Command line expense tracker (data stored in a CSV file).

The file emma_expenses.csv shipped with the project already contains a full
year of expenses, so the statistics are meaningful from the first run.
"""

import csv
import os
from datetime import datetime

FILENAME = "emma_expenses.csv"  # or "personnal_expenses.csv"
COLUMNS = ["date", "category", "description", "amount"]


class Expense:
    """One expense, with its values already converted to the right type.

    A CSV file only stores text, so the amount arrives as "68.72" and not as a
    number: the conversion is done once, here.
    """

    def __init__(self, date, category, description, amount):
        self.date = date  # kept as text, e.g. "05/03/2025"
        self.category = category
        self.description = description
        self.amount = float(amount)

    def to_row(self):
        """Return the expense as a list of texts, ready to be written in the CSV."""
        return [self.date, self.category, self.description, f"{self.amount:.2f}"]


def read_expenses():
    """Return the list of expenses saved in the CSV file."""
    if not os.path.exists(FILENAME):
        return []

    expenses = []

    with open(FILENAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Each row is a dictionary of texts: we turn it into an Expense.
        for row in reader:
            expense = Expense(
                row["date"], row["category"], row["description"], row["amount"]
            )
            expenses.append(expense)

    return expenses


def save_expense(expense):
    """Append one expense at the end of the CSV file."""
    file_exists = os.path.exists(FILENAME)

    with open(FILENAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # A brand new file needs its header line first.
        if not file_exists:
            writer.writerow(COLUMNS)

        writer.writerow(expense.to_row())


def show_history():
    """Display every saved expense along with the total."""
    expenses = read_expenses()

    if not expenses:
        print("No expense saved yet, add one first.\n")
        return

    print("\n--- Expense history ---")
    header = f"{'Date':<12}{'Category':<20}{'Description':<30}{'Amount':>10}"
    print(header)

    total = 0
    for expense in expenses:
        line = (
            f"{expense.date:<12}{expense.category:<20}"
            f"{expense.description:<30}{expense.amount:>10.2f}"
        )
        print(line)
        total += expense.amount

    print(f"\nTotal: {total:.2f} EUR over {len(expenses)} expense(s).\n")


def add_expense():
    """Ask for the details of an expense and append it to the CSV file."""
    category = input("Category (e.g. groceries, transport): ").strip()
    description = input("Description: ").strip()

    # In French a comma is used for decimals, but Python needs a dot.
    answer = input("Amount in euros: ").strip().replace(",", ".")

    try:
        amount = float(answer)
    except ValueError:
        print("Invalid amount, the expense was not saved.\n")
        return

    today = datetime.now().strftime("%d/%m/%Y")
    expense = Expense(today, category, description, amount)
    save_expense(expense)

    print(f"Expense of {expense.amount:.2f} EUR saved.\n")


def show_menu():
    """Display the available choices."""
    print("=== Expense tracker ===")
    print("1. Show history")
    print("2. Add an expense")
    print("3. Quit")


def main():
    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_history()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            print("See you soon!")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 3.\n")


if __name__ == "__main__":
    main()
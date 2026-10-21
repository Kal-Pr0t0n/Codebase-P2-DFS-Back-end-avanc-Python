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


def show_statistics():
    """Affiche le montant des dépenses par catégorie"""
    # E1. Récupération des valeurs : 
    expenses = read_expenses()

    if not expenses: 
        print("Aucune dépense enregistrée.")
        return
    
    # E2. On parcourt toutes les données et fait la sommes par catégorie 
    categories = {}
    months = set()
    for expense in expenses:
        if expense.category not in categories.keys():
            categories[expense.category] = [expense.amount, 0] 
        else:
            categories[expense.category][0] += expense.amount
        months.add(expense.date[3:])
    total_months = len(months)
    for category in categories:
        categories[category][1] = categories[category][0] / total_months

    # E3. Affiche le résultat sous forme de tableau
    print("\n --- Expense statistics ---")
    
    max_spacement = len('Category')
    max_spacement_total = len("   Total (€)")
    max_spacement_moy_month = len("   Moyenne / mois")
    for category in sorted(categories.keys()):
        if len(category) > max_spacement:
            max_spacement = len(category)
        if len(str(categories[category][0])) > max_spacement_total:
            max_spacement_total = len(str(categories[category][0]))
        if (len(str(categories[category][1]))) > max_spacement_moy_month:
            max_spacement_moy_month = len(str(categories[category][1]))

    max_spacement += 4
    total_all = 0
    corps_tb = ""
    for category in sorted(categories.keys()):
        total = categories[category][0]
        avg = categories[category][1]
        
        total_str = f"{total:.2f}"
        avg_str = f"{avg:.2f}"

        corps_tb += (
            f"| {category}{' ' * (max_spacement - len(category))} "
            f"|{' ' * (
                max_spacement_total 
                - len(f" {total_str} € " )-2
                )} {total_str} € "
            f"|{" " * (
                max_spacement_moy_month 
                - len(f" {avg_str} € ")
                )}{avg_str} € |\n"
        )
         
        total_all += categories[category][0]
    moy_total_months = total_all / total_months

    
    header = (
        " " + "-" * (max_spacement - 2) +
        "-" * (max_spacement_total+3) +
        "-" * (max_spacement_moy_month) + " \n"
    )
    header += (
(
            f"| Category{' ' * (max_spacement - len("Category"))} "
            f"|{' ' * (
                max_spacement_total 
                - len(f" {"Total (€)"}   " )
                )} Total (€) "
            f"|{" " * (
                max_spacement_moy_month 
                - len(f" Moyenne / Mois ")
                )}Moyenne / Mois |\n"
        )
    )
    header += (
        " " + "-" * (max_spacement - 2) +
        "-" * (max_spacement_total + 3) +
        "-" * (max_spacement_moy_month) + " "
    )    

    footer =( 
        " " + "-" * (max_spacement - 2) 
        + "-" * (max_spacement_total+3)
        + "-" * (max_spacement_moy_month) + " \n")
    footer += (
        f"| {' '*(
            max_spacement + max_spacement_total 
            - len(f"Total des dépenses : {total_all:.2f} € "))}"
        f"Total des dépenses : {total_all:.2f}  €|{' ' * len(f"{moy_total_months:.2f} "
        f"€/Mois " + " |")}|\n") 
    footer += (f"| {' ' * (max_spacement + max_spacement_total 
        - len(f"Nombre de mois couverts : {total_months} "))}"
        f"Nombre de mois couverts : {total_months} | {moy_total_months:.2f} "
        f"€/Mois " + " |\n")
    footer += ( 
        " " + "-"*(max_spacement - 2) 
        + "-" * (max_spacement_total + 3)
        + "-" * (max_spacement_moy_month) + " ")      

    print(header)
    print(corps_tb[:len(corps_tb) - 1])
    print(footer)  


def show_menu():
    """Display the available choices."""
    print("=== Expense tracker ===")
    print("1. Show history")
    print("2. Add an expense")
    print("")
    print("3. Show statistics")
    print("")
    print("q. Quit")


def main():
    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_history()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_statistics()
        elif choice == "q":
            print("See you soon!")
            break
        else:
            print(
                "Invalid choice, please enter a number between 1 and 3"
                " (or q to quit).\n"
                )


if __name__ == "__main__":
    main()
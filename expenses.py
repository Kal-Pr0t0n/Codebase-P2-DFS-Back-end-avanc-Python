"""Command line expense tracker (data stored in a CSV file).

The file emma_expenses.csv shipped with the project already contains a full
year of expenses, so the statistics are meaningful from the first run.
"""

import csv
import os
from datetime import datetime
import math

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


def get_moyen_mensual_expenses():
    """Récupère la liste des dépenses et calcul la moyenne mensuelle dépensée"""
    moyenne_mensuelle = 0
    expenses = read_expenses()
    
    if not expenses: 
        print("Aucune dépense enregistrée.")
        return moyenne_mensuelle

    months = set()
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount
        months.add(expense.date[3:])
    
    total_months = len(months)
    return (total_expenses / total_months)
    

def simulate_buy_car():
    """Simulation l'achat d'un véhicule
    
    [!] Attention : La notion de salaire ou de revenu fixe n'étant pas présent dans
    le projet initiale et le fichier .csv ne contenant que des dépenses, la valeur du 
    salaire mensuel sera donc demandé à l'utilisateur (avec une valeur initiale propsoée
    à 2 500€)
    """
    # E1. Récupération des valeurs initiales permettant la simulation
    print(" == SIMULATION D'ACHAT D'UN VEHICULE ==\n\n")

    print(
        "Pour permettre cette simulation, veuillez renseigner "
        "les informations suivantes:")

    monthly_salary = input("Votre salaire mensuel (2 500€ par défaut): ").strip()

    if monthly_salary == "":
        monthly_salary = 2500
    try:
        monthly_salary = float(monthly_salary)
    except ValueError:
        print("Montant invalide, veuillez saisir une valeur numérique.\n")
        return

    car_value = input("Veuillez indiquer le montant du véhicule à acquérir : ").strip()

    try:
        car_value = float(car_value)
    except ValueError:
        print("Montant invalide, veuillez saisir une valeur numérique.\n")
        return
    if car_value <= 0:
        print("Le montant du véhicule doit être supérieur à 0!\n")
        return
    
    print("------------------------------------------")
    print(f"Salaire Mensuel : {monthly_salary:.2f} €")
    print(f"Valeur du véhicule : {car_value:.2f} €")
    print("------------------------------------------")

    # E2. Récupération des valeurs de dépenses mensuelles (moyennes mensuelle)
    moyenne_mensuelle = get_moyen_mensual_expenses()
    print(f"Moyenne mensuelles des dépenses : {moyenne_mensuelle:.2f} € / Mois")
    print("------------------------------------------")
    # E3. Calcul de l'épargne, des mensualités et des mensualités maximales possibles
    epargne_restant = monthly_salary - moyenne_mensuelle
    if epargne_restant <= 0:
        print("Vous dépensez plus que votre salaire, impossible d'acheter une voiture.")
        return
    print(f"Epargne restante : {epargne_restant:.2f} € / Mois")
    mois_necessaires = car_value / epargne_restant
    print(
        "Nombre de mois restant pour épargner la totalité de la voiture :"
        f" {math.ceil(mois_necessaires)} mois"
        )
    print("==============FIN DE LA SIMULATION =======================")


def get_moyen_mensual_of_specific_expense(categorie: str="housing"):
    """Récupère la liste des dépenses et calcul la moyenne mensuelle dépensée
    pour une catégorie précise. [par défaut "logement"]
    """
    expenses = read_expenses()
    
    if not expenses: 
        print("Aucune dépense enregistrée.")
        return 0,0
    
    months = set()
    total_expenses = 0
    total_expenses_by_category = 0
    for expense in expenses:
        if expense.category == categorie:
            total_expenses_by_category += expense.amount
        total_expenses += expense.amount
        months.add(expense.date[3:])
    
    total_months = len(months)
    return (total_expenses / total_months), (total_expenses_by_category / total_months)
    
    

def simulate_mortgage():
    """Simulation d'un prêt immobilier
    
    [!] Attention : La notion de salaire ou de revenu fixe n'étant pas présent dans
    le projet initiale et le fichier .csv ne contenant que des dépenses, la valeur du 
    salaire mensuel sera donc demandé à l'utilisateur (avec une valeur initiale propsoée
    à 2 500€)
    """

    # E1. Demande des informations nécessaires à la simulation
    print(" == SIMULATION D'UNE DEMANDE DE PRÊT IMMOBILIER ==")
    monthly_salary = input(
        "Veuillez préciser votre salaire mensuel "
        "(2 500€ par défaut): ").strip()

    if monthly_salary == "":
        monthly_salary = 2500
    try:
        monthly_salary = float(monthly_salary)
    except ValueError:
        print("Montant invalide, veuillez saisir une valeur numérique.\n")
        return

    if monthly_salary <= 0:
        print("Le salaire doit être supérieur à 0!\n")
        return

    # E2. Récupération du montant moyen de la catégorie "Logement" 
    #     et calcul de l'épargne disponible
    total_expense, housing_average = get_moyen_mensual_of_specific_expense()
    print("\n")
    print(f"Moyenne mensuelle des dépenses de logement : {housing_average:.2f} € / Mois")
    print(f"Moyenne mensuelle de toutes les dépenses : {total_expense:.2f} € / Mois")
    print("------------------------------------------")
    epargne_restant = monthly_salary - (total_expense - housing_average)
    if epargne_restant <= 0:
        print("Vous dépensez plus que votre salaire, impossible de contracter un prêt.")
        return
    print(f"Epargne possible (en retirant le montant du logement actuel) : {epargne_restant:.2f} € / Mois")
    print("------------------------------------------")

    # E3. Calcul du montant empruntable à partir de la formule fournie
    #     Formule : Montant empruntable = (Salaire Mensuel - Dépenses Mensuelles) 
    #               * 12 * Taux d'endettement maximum
    #     Taux d'endettement maximum = 35 %

    print(
        "Formule : Montant empruntable = (Salaire Mensuel - Dépenses Mensuelles) * 12 "
        "* Taux d'endettement maximum"
        )
    montant_empruntable = epargne_restant * 12 * 0.35
    print(f"Pour une mensualité de {(montant_empruntable/12):.2f} € mensuelle")
    print(f"soit un Montant empruntable maximum (sur 25 ans):  {(montant_empruntable *25):.2f} €")
    print("------------------------------------------")


def show_menu():
    """Display the available choices."""
    print("==========================================================")
    print("=== Expense tracker ===")
    print("1. Show history")
    print("2. Add an expense")
    print("")
    print("3. Statistiques ")
    print("4. Simulation achat d'une voiture")
    print("5. Simulation prêt immobilier")
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
        elif choice == "4":
            simulate_buy_car()
        elif choice == "5":
            simulate_mortgage()
        elif choice == "q":
            print("See you soon!")
            break
        else:
            print(
                "Invalid choice, please enter a number between 1 and 5"
                " (or q to quit).\n"
                )


if __name__ == "__main__":
    main()
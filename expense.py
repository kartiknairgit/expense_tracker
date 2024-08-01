import datetime
import calendar
import json
import os
from colorama import init, Fore, Style

init(autoreset=True)  

def print_fancy_header(text):
    width = 50
    print(Fore.CYAN + Style.BRIGHT + "=" * width)
    print(Fore.CYAN + Style.BRIGHT + text.center(width))
    print(Fore.CYAN + Style.BRIGHT + "=" * width)

def print_menu_option(number, text):
    print(Fore.GREEN + f"  {number}. " + Fore.WHITE + text)

def print_submenu_option(number, text):
    print(Fore.YELLOW + f"  {number}. " + Fore.WHITE + text)

def print_info(text):
    print(Fore.BLUE + Style.BRIGHT + text)

def print_warning(text):
    print(Fore.RED + Style.BRIGHT + text)

class DailyBudgetTracker:
    def __init__(self):
        self.base_folder = "budget_data"
        self.current_date = datetime.date.today()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        self.current_month_name = calendar.month_name[self.current_month]
        self.current_folder = os.path.join(self.base_folder, f"{self.current_year}_{self.current_month_name}")
        self.transactions_file = os.path.join(self.current_folder, "transactions.json")
        self.budget_file = os.path.join(self.current_folder, "budget.json")

    def create_month_folder(self):
        os.makedirs(self.current_folder, exist_ok=True)

    def set_budget(self, amount):
        budget_data = {"budget": amount, "remaining": amount}
        with open(self.budget_file, 'w') as file:
            json.dump(budget_data, file)
        print(f"Budget of ${amount:.2f} set for {self.current_month_name} {self.current_year}.")

    def load_budget(self):
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as file:
                return json.load(file)
        return None

    def save_transaction(self, category, amount):
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []

        transaction = {
            "date": str(self.current_date),
            "category": category,
            "amount": amount
        }
        transactions.append(transaction)

        with open(self.transactions_file, 'w') as file:
            json.dump(transactions, file)

    def update_budget(self, amount):
        budget_data = self.load_budget()
        if budget_data:
            budget_data["remaining"] -= amount
            with open(self.budget_file, 'w') as file:
                json.dump(budget_data, file)

    def add_expense(self, category, amount):
        self.save_transaction(category, amount)
        self.update_budget(amount)
        budget_data = self.load_budget()
        if budget_data:
            remaining = budget_data["remaining"]
            print(f"Expense added. Remaining budget: " + Fore.GREEN + f"${remaining:.2f}" + Style.RESET_ALL)
        self.check_budget()

    def check_budget(self):
        budget_data = self.load_budget()
        if budget_data:
            remaining = budget_data["remaining"]
            budget = budget_data["budget"]
            if remaining <= 0:
                print_warning("WARNING: You have exceeded your budget for this month!")
            elif remaining <= budget * 0.1:
                print_warning(f"WARNING: You are within 10% of your budget limit for this month!")
                print(f"Remaining: " + Fore.RED + f"${remaining:.2f}" + Style.RESET_ALL)

    def get_expense_summary(self):
        budget_data = self.load_budget()
        if not budget_data:
            print_warning("No budget data available for this month.")
            return

        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []

        print_fancy_header(f"Expense Summary for {self.current_month_name} {self.current_year}")
        total_expenses = 0
        category_expenses = {}

        for transaction in transactions:
            category = transaction["category"]
            amount = transaction["amount"]
            total_expenses += amount
            if category not in category_expenses:
                category_expenses[category] = 0
            category_expenses[category] += amount

        for category, amount in category_expenses.items():
            print(f"{category}: " + Fore.RED + f"${amount:.2f}" + Style.RESET_ALL)

        print(f"\nTotal Expenses: " + Fore.RED + f"${total_expenses:.2f}" + Style.RESET_ALL)
        remaining = budget_data['remaining']
        print(f"Remaining Budget: " + Fore.GREEN + f"${remaining:.2f}" + Style.RESET_ALL)

        # Add reminder when 10% or less of the budget is left
        if remaining <= budget_data['budget'] * 0.1:
            print_warning("REMINDER: You have 10% or less of your original budget left!")

def choose_month():
    print_fancy_header("Available Months")
    for i, month in enumerate(calendar.month_name[1:], 1):
        print_submenu_option(i, month)
    while True:
        choice = input(Fore.YELLOW + "\nChoose a month (1-12): " + Fore.WHITE)
        if choice.isdigit() and 1 <= int(choice) <= 12:
            return int(choice)
        print_warning("Invalid choice. Please enter a number between 1 and 12.")

def main():
    tracker = DailyBudgetTracker()

    while True:
        print_fancy_header("Daily Budget Tracker")
        print_info(f"Current Date: {tracker.current_date}")
        print_menu_option(1, "Yes, I have set a budget for this month")
        print_menu_option(2, "No, I need to set a budget")
        print_menu_option(3, "Exit")
        choice = input(Fore.GREEN + "\nEnter your choice (1-3): " + Fore.WHITE)

        if choice == '1':
            month = choose_month()
            tracker.current_month = month
            tracker.current_month_name = calendar.month_name[month]
            tracker.current_folder = os.path.join(tracker.base_folder, f"{tracker.current_year}_{tracker.current_month_name}")
            tracker.transactions_file = os.path.join(tracker.current_folder, "transactions.json")
            tracker.budget_file = os.path.join(tracker.current_folder, "budget.json")

            if not os.path.exists(tracker.current_folder):
                print_warning(f"Budget hasn't been set for {tracker.current_month_name} {tracker.current_year}.")
                set_budget = input(Fore.YELLOW + "Would you like to set a budget now? (y/n): " + Fore.WHITE).lower()
                if set_budget == 'y':
                    tracker.create_month_folder()
                    amount = float(input(Fore.YELLOW + f"Enter budget for {tracker.current_month_name} {tracker.current_year}: $" + Fore.WHITE))
                    tracker.set_budget(amount)
                else:
                    continue
        elif choice == '2':
            tracker.create_month_folder()
            amount = float(input(Fore.YELLOW + f"Enter budget for {tracker.current_month_name} {tracker.current_year}: $" + Fore.WHITE))
            tracker.set_budget(amount)
        elif choice == '3':
            print_info("Good call kartzie")
            break
        else:
            print_warning("Invalid choice. Please try again.")
            continue

        while True:
            print_fancy_header(f"Current Month: {tracker.current_month_name} {tracker.current_year}")
            print_submenu_option(1, "Add Expense")
            print_submenu_option(2, "View Expense Summary")
            print_submenu_option(3, "Back to Main Menu")
            subchoice = input(Fore.YELLOW + "\nEnter your choice (1-3): " + Fore.WHITE)

            if subchoice == '1':
                category = input(Fore.YELLOW + "Enter expense category: " + Fore.WHITE)
                amount = float(input(Fore.YELLOW + "Enter expense amount: $" + Fore.WHITE))
                tracker.add_expense(category, amount)
            elif subchoice == '2':
                tracker.get_expense_summary()
            elif subchoice == '3':
                break
            else:
                print_warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
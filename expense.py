import sys
import os
import json
import calendar
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, 
                             QMessageBox, QStackedWidget, QHBoxLayout, 
                             QGridLayout, QProgressBar)
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar

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
        self.create_month_folder()
        budget_data = {"budget": amount, "remaining": amount}
        with open(self.budget_file, 'w') as file:
            json.dump(budget_data, file)
        return f"Budget of ${amount:.2f} set for {self.current_month_name} {self.current_year}."

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
            return f"Expense added. Remaining budget: ${remaining:.2f}"
        return "Expense added, but couldn't update budget."

    def check_budget(self):
        budget_data = self.load_budget()
        if budget_data:
            remaining = budget_data["remaining"]
            budget = budget_data["budget"]
            if remaining <= 0:
                return "WARNING: You have exceeded your budget for this month!"
            elif remaining <= budget * 0.1:
                return f"WARNING: You are within 10% of your budget limit for this month! Remaining: ${remaining:.2f}"
        return ""

    def get_expense_summary(self):
        budget_data = self.load_budget()
        if not budget_data:
            return "No budget data available for this month."

        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []

        summary = f"Expense Summary for {self.current_month_name} {self.current_year}\n\n"
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
            summary += f"{category}: ${amount:.2f}\n"

        summary += f"\nTotal Expenses: ${total_expenses:.2f}\n"
        remaining = budget_data['remaining']
        summary += f"Remaining Budget: ${remaining:.2f}\n"

        if remaining <= budget_data['budget'] * 0.1:
            summary += "\nREMINDER: You have 10% or less of your original budget left!"

        return summary

class BudgetTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tracker = DailyBudgetTracker()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Daily Budget Tracker')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.create_main_menu()
        self.create_budget_page()
        self.create_expense_page()
        self.create_summary_page()

        # Apply custom styling
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f7f7;
                color: #333;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)

    def create_main_menu(self):
        menu_page = QWidget()
        menu_layout = QVBoxLayout(menu_page)

        title = QLabel('Daily Budget Tracker')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 16))
        menu_layout.addWidget(title)

        btn_set_budget = QPushButton('Set Budget')
        btn_set_budget.setIcon(QIcon("icons/budget.png"))
        btn_set_budget.clicked.connect(self.show_budget_page)
        menu_layout.addWidget(btn_set_budget)

        btn_add_expense = QPushButton('Add Expense')
        btn_add_expense.setIcon(QIcon("icons/expense.png"))
        btn_add_expense.clicked.connect(self.show_expense_page)
        menu_layout.addWidget(btn_add_expense)

        btn_view_summary = QPushButton('View Summary')
        btn_view_summary.setIcon(QIcon("icons/summary.png"))
        btn_view_summary.clicked.connect(self.show_summary_page)
        menu_layout.addWidget(btn_view_summary)

        self.stacked_widget.addWidget(menu_page)

    def create_budget_page(self):
        budget_page = QWidget()
        layout = QVBoxLayout(budget_page)

        title = QLabel('Set Budget')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 14))
        layout.addWidget(title)

        self.month_combo = QComboBox()
        self.month_combo.addItems(calendar.month_name[1:])
        layout.addWidget(self.month_combo)

        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText('Enter budget amount')
        layout.addWidget(self.budget_input)

        btn_set = QPushButton('Set Budget')
        btn_set.clicked.connect(self.set_budget)
        layout.addWidget(btn_set)

        btn_back = QPushButton('Back to Main Menu')
        btn_back.clicked.connect(self.show_main_menu)
        layout.addWidget(btn_back)

        self.stacked_widget.addWidget(budget_page)

    def create_expense_page(self):
        expense_page = QWidget()
        layout = QVBoxLayout(expense_page)

        title = QLabel('Add Expense')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 14))
        layout.addWidget(title)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Enter expense category')
        layout.addWidget(self.category_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter expense amount')
        layout.addWidget(self.amount_input)

        btn_add = QPushButton('Add Expense')
        btn_add.clicked.connect(self.add_expense)
        layout.addWidget(btn_add)

        btn_back = QPushButton('Back to Main Menu')
        btn_back.clicked.connect(self.show_main_menu)
        layout.addWidget(btn_back)

        self.stacked_widget.addWidget(expense_page)

    def create_summary_page(self):
        summary_page = QWidget()
        layout = QVBoxLayout(summary_page)

        self.summary_label = QLabel('Expense Summary')
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.summary_label.setFont(QFont('Arial', 14))
        layout.addWidget(self.summary_label)

        self.summary_text = QLabel()
        self.summary_text.setWordWrap(True)
        layout.addWidget(self.summary_text)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        btn_back = QPushButton('Back to Main Menu')
        btn_back.clicked.connect(self.show_main_menu)
        layout.addWidget(btn_back)

        self.stacked_widget.addWidget(summary_page)

    def show_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_budget_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_expense_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_summary_page(self):
        self.summary_text.setText(self.tracker.get_expense_summary())
        budget_data = self.tracker.load_budget()
        if budget_data:
            total_budget = budget_data['budget']
            remaining_budget = budget_data['remaining']
            percentage_used = int((total_budget - remaining_budget) / total_budget * 100)
            self.progress_bar.setValue(percentage_used)
        self.stacked_widget.setCurrentIndex(3)


    def set_budget(self):
        month = self.month_combo.currentIndex() + 1
        amount = float(self.budget_input.text())
        self.tracker.current_month = month
        self.tracker.current_month_name = calendar.month_name[month]
        self.tracker.current_folder = os.path.join(self.tracker.base_folder, f"{self.tracker.current_year}_{self.tracker.current_month_name}")
        self.tracker.transactions_file = os.path.join(self.tracker.current_folder, "transactions.json")
        self.tracker.budget_file = os.path.join(self.tracker.current_folder, "budget.json")
        result = self.tracker.set_budget(amount)
        QMessageBox.information(self, "Budget Set", result)
        self.show_main_menu()

    def add_expense(self):
        category = self.category_input.text()
        amount = float(self.amount_input.text())
        result = self.tracker.add_expense(category, amount)
        QMessageBox.information(self, "Expense Added", result)
        warning = self.tracker.check_budget()
        if warning:
            QMessageBox.warning(self, "Budget Warning", warning)
        self.category_input.clear()
        self.amount_input.clear()
        self.show_main_menu()

def main():
    app = QApplication(sys.argv)
    ex = BudgetTrackerGUI()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
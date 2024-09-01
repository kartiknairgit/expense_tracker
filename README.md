# Daily Budget Tracker

## Overview

The **Daily Budget Tracker** is a PyQt6-based desktop application designed to help users manage their daily expenses and monitor their monthly budget. The application allows users to set a monthly budget, add expenses by category, and view a summary of their expenditures. It also features warnings when the budget is close to being exhausted, helping users stay on track financially.

## Features

- **Set Monthly Budget**: Users can specify their budget for the month, which will be saved and used to track their expenses.
- **Add Expenses**: Users can record their daily expenses by entering the amount and category.
- **Expense Summary**: View a detailed summary of your monthly expenses, categorized and compared against the set budget.
- **Budget Alerts**: Receive warnings when you are close to exceeding your budget or when you have exceeded it.

## Installation

### Prerequisites

- Python 3.x
- PyQt6
- Calendar
- Datetime

### Setting Up

1. Clone or download the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages:
    ```bash
    pip install PyQt6
    ```
4. Run the application:
    ```bash
    python main.py
    ```

## How to Use

### Main Menu

Upon launching the application, you will be presented with three main options:

- **Set Budget**: Set your monthly budget.
- **Add Expense**: Add a new expense by entering the category and amount.
- **View Summary**: View a summary of your monthly expenses, including a progress bar showing how much of your budget has been used.

### Setting Your Budget

1. Click on the "Set Budget" button in the main menu.
2. Select the month for which you want to set the budget from the dropdown menu.
3. Enter the budget amount.
4. Click the "Set Budget" button to save your budget.

### Adding an Expense

1. Click on the "Add Expense" button in the main menu.
2. Enter the category of the expense (e.g., groceries, entertainment).
3. Enter the amount spent.
4. Click the "Add Expense" button to save the expense. If the expense causes your remaining budget to be low or exceeded, a warning message will be displayed.

### Viewing Expense Summary

1. Click on the "View Summary" button in the main menu.
2. A summary of all expenses for the selected month will be displayed, along with a progress bar indicating how much of your budget has been used.

### Navigation

- Use the "Back to Main Menu" button on any page to return to the main menu.

## File Structure

- **budget_data/**: Folder where monthly budget and transaction data are stored.
- **icons/**: Folder containing icon files used in the application.
- **main.py**: Main script that runs the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- PyQt6 for providing the graphical user interface framework.

## Contact

For any questions or suggestions, please contact kartik.n.1101@gmail.com

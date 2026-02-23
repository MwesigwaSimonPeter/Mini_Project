"""

PERSONAL BUDGET MANAGER

A command-line financial management tool designed for
first-year university students.

This program allows a user to:
1. Set a weekly budget.
2. Record a user-defined number of transactions.
3. Monitor expenses in real time.
4. Receive warnings when exceeding the budget.
5. Generate a final financial summary report.

"""

from dataclasses import dataclass

# DATA CLASS: Represents a single financial transaction

@dataclass
class Transaction:
    description: str
    amount: float



# CLASS: BudgetManager
# Responsible for handling all financial calculations

class BudgetManager:

    def __init__(self, budget: float):
        # Validate budget before storing it
        self._validate_budget(budget)
        self.initial_budget = budget
        self.transactions = []

    # Private method to ensure budget is non-negative
    def _validate_budget(self, budget: float):
        if budget < 0:
            raise ValueError("Budget must be non-negative.")

    # Adds a transaction after validation
    def add_transaction(self, transaction: Transaction):
        if transaction.amount < 0:
            raise ValueError("Transaction amount cannot be negative.")
        self.transactions.append(transaction)

    # Property to calculate total expenses dynamically
    @property
    def total_expenses(self) -> float:
        return sum(t.amount for t in self.transactions)

    # Property to calculate remaining balance
    @property
    def remaining_balance(self) -> float:
        return self.initial_budget - self.total_expenses

    # Checks if spending has exceeded budget
    def is_budget_exceeded(self) -> bool:
        return self.total_expenses > self.initial_budget

    # Generates final financial report
    def generate_summary(self) -> str:
        summary_lines = []
        summary_lines.append("\n========== FINAL FINANCIAL SUMMARY ==========")
        summary_lines.append(f"Initial Budget: UGX {self.initial_budget:.2f}")
        summary_lines.append(f"Total Expenses: UGX {self.total_expenses:.2f}")

        if self.remaining_balance >= 0:
            summary_lines.append(
                f"Remaining Balance: UGX {self.remaining_balance:.2f}"
            )
        else:
            summary_lines.append(
                f"Deficit: UGX {abs(self.remaining_balance):.2f}"
            )

        summary_lines.append("\nTransaction Log:")
        for index, transaction in enumerate(self.transactions, start=1):
            summary_lines.append(
                f"{index}. {transaction.description} - UGX {transaction.amount:.2f}"
            )

        return "\n".join(summary_lines)



# INPUT FUNCTIONS
def get_valid_budget() -> float:
    """
    Prompts the user to enter a valid, non-negative budget.
    Keeps prompting until a valid number is entered.
    """
    while True:
        try:
            budget = float(input("Enter your weekly budget (UGX): "))
            if budget < 0:
                print("Budget cannot be negative. Try again.")
                continue
            return budget
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_transaction_input() -> Transaction:
    """
    Prompts the user for transaction description and amount.
    Returns a Transaction object.
    """
    description = input("Enter transaction description: ")
    while True:
        try:
            amount = float(input("Enter transaction amount (UGX): "))
            if amount < 0:
                print("Amount cannot be negative. Try again.")
                continue
            return Transaction(description, amount)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_number_of_transactions() -> int:
    """
    Prompts the user for how many transactions they want to log.
    Ensures a positive integer is entered.
    """
    while True:
        try:
            n = int(input("Enter the number of transactions you want to log: "))
            if n <= 0:
                print("Number must be greater than zero. Try again.")
                continue
            return n
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



# MAIN PROGRAM CONTROLLER

def main():
    print("Welcome to the Personal Budget Manager\n")

    # Step 1: Initialize budget
    budget = get_valid_budget()
    manager = BudgetManager(budget)

    # Step 2: Ask user how many transactions they want
    transaction_count_limit = get_number_of_transactions()
    transaction_count = 0

    # Step 3: Loop to collect transactions
    while transaction_count < transaction_count_limit:
        transaction = get_transaction_input()
        manager.add_transaction(transaction)
        transaction_count += 1

        # Real-time calculations
        total = manager.total_expenses
        remaining = manager.remaining_balance

        # Display mini-report after each transaction
        print("\n--- Transaction Added ---")
        print(f"{transaction.description:<25} UGX {transaction.amount:>10.2f}")
        print(f"{'Total Expenses':<25} UGX {total:>10.2f}")
        if remaining >= 0:
            print(f"{'Remaining Balance':<25} UGX {remaining:>10.2f}")
        else:
            print(f"{'⚠ Deficit':<25} UGX {abs(remaining):>10.2f}")
        print("----------------------------\n")

    # Step 4: Final financial summary
    print(manager.generate_summary())



# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()
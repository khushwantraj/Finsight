from datetime import datetime
from app.models import Transaction, DashboardStats

# Sample transactions data
sample_transactions = [
    Transaction(
        id=1,
        transaction_date=datetime(2024, 1, 15, 10, 30, 0),
        description="Salary Deposit",
        amount=5000.00,
        category="Income",
        account_type="Checking"
    ),
    Transaction(
        id=2,
        transaction_date=datetime(2024, 1, 16, 14, 20, 0),
        description="Grocery Store",
        amount=-85.50,
        category="Food",
        account_type="Checking"
    ),
    Transaction(
        id=3,
        transaction_date=datetime(2024, 1, 17, 9, 0, 0),
        description="Gas Station",
        amount=-45.00,
        category="Transportation",
        account_type="Credit Card"
    ),
    Transaction(
        id=4,
        transaction_date=datetime(2024, 1, 18, 16, 45, 0),
        description="Electric Bill",
        amount=-120.00,
        category="Utilities",
        account_type="Checking"
    ),
    Transaction(
        id=5,
        transaction_date=datetime(2024, 1, 19, 12, 30, 0),
        description="Restaurant",
        amount=-60.00,
        category="Food",
        account_type="Credit Card"
    ),
    Transaction(
        id=6,
        transaction_date=datetime(2024, 1, 20, 10, 15, 0),
        description="Online Shopping",
        amount=-150.00,
        category="Shopping",
        account_type="Credit Card"
    ),
    Transaction(
        id=7,
        transaction_date=datetime(2024, 1, 22, 8, 0, 0),
        description="Gym Membership",
        amount=-50.00,
        category="Health",
        account_type="Checking"
    ),
    Transaction(
        id=8,
        transaction_date=datetime(2024, 1, 23, 18, 30, 0),
        description="Freelance Payment",
        amount=800.00,
        category="Income",
        account_type="Checking"
    ),
    Transaction(
        id=9,
        transaction_date=datetime(2024, 1, 25, 13, 0, 0),
        description="Coffee Shop",
        amount=-15.50,
        category="Food",
        account_type="Credit Card"
    ),
    Transaction(
        id=10,
        transaction_date=datetime(2024, 1, 28, 11, 20, 0),
        description="Internet Bill",
        amount=-80.00,
        category="Utilities",
        account_type="Checking"
    ),
]

# Sample dashboard stats
sample_dashboard_stats = DashboardStats(
    total_income=5800.00,
    total_expenses=606.00,
    net_savings=5194.00,
    account_balance=12500.00
)

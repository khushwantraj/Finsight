from pydantic import BaseModel, Field


class DashboardStats(BaseModel):
    total_income: float = Field(..., serialization_alias="totalIncome")
    total_expenses: float = Field(..., serialization_alias="totalExpenses")
    net_savings: float = Field(..., serialization_alias="netSavings")
    account_balance: float = Field(..., serialization_alias="accountBalance")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "total_income": 5000.00,
                "total_expenses": 3500.00,
                "net_savings": 1500.00,
                "account_balance": 12500.00
            }
        }

export interface Transaction {
  id: number;
  transactionDate: string;
  description: string;
  amount: number;
  category: string;
  accountType: string;
}

export interface DashboardStats {
  totalIncome: number;
  totalExpenses: number;
  netSavings: number;
  accountBalance: number;
}

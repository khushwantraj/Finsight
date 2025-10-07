import { Transaction, DashboardStats } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = {
  // Dashboard endpoints
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await fetch(`${API_BASE_URL}/api/dashboard`);
    if (!response.ok) {
      throw new Error('Failed to fetch dashboard stats');
    }
    return response.json();
  },

  // Transaction endpoints
  async getTransactions(limit: number = 10, offset: number = 0): Promise<Transaction[]> {
    const response = await fetch(
      `${API_BASE_URL}/api/transactions?limit=${limit}&offset=${offset}`
    );
    if (!response.ok) {
      throw new Error('Failed to fetch transactions');
    }
    return response.json();
  },

  async getTransaction(id: number): Promise<Transaction> {
    const response = await fetch(`${API_BASE_URL}/api/transactions/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch transaction');
    }
    return response.json();
  },
};

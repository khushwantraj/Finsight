import React, { useEffect, useState } from 'react';
import { DashboardStats } from '../types';
import { api } from '../services/api';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.getDashboardStats();
        setStats(data);
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!stats) return <div className="error">No data available</div>;

  return (
    <div className="dashboard">
      <h1>Financial Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Income</h3>
          <p className="amount positive">${stats.totalIncome.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Total Expenses</h3>
          <p className="amount negative">${stats.totalExpenses.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Net Savings</h3>
          <p className="amount positive">${stats.netSavings.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Account Balance</h3>
          <p className="amount">${stats.accountBalance.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};

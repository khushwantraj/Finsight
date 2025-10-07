import React from 'react';
import { Dashboard } from './components/Dashboard';
import { TransactionList } from './components/TransactionList';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Finsight</h1>
        <p>Your Financial Insights Dashboard</p>
      </header>
      <main>
        <Dashboard />
        <TransactionList />
      </main>
    </div>
  );
}

export default App;

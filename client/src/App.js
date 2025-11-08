import React, { useState } from 'react';
import './App.css';

const inflationCategories = [
  'Food & non-alcoholic beverages',
  'Alcohol & tobacco',
  'Clothing & footwear',
  'Housing',
  'Utilities',
  'Household durables and daily use items',
  'Health',
  'Transport',
  'Communications',
  'Recreation and culture',
  'Education',
  'Other',
];

function App() {
  const [income, setIncome] = useState('');
  const [year1, setYear1] = useState(
    inflationCategories.reduce((acc, category) => ({ ...acc, [category]: '' }), {})
  );
  const [year2, setYear2] = useState(
    inflationCategories.reduce((acc, category) => ({ ...acc, [category]: '' }), {})
  );
  const [results, setResults] = useState(null);

  const handleCalculate = async () => {
    const year1Data = Object.fromEntries(
      Object.entries(year1).map(([key, value]) => [key, Number(value) || 0])
    );
    const year2Data = Object.fromEntries(
      Object.entries(year2).map(([key, value]) => [key, Number(value) || 0])
    );

    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        income: Number(income) || 0,
        year1: year1Data,
        year2: year2Data,
      }),
    });

    const data = await response.json();
    setResults(data);
  };

  const handleExport = () => {
    const dataStr = JSON.stringify({ income, year1, year2, results }, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = 'personal-inflation-data.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Personal Inflation Calculator</h1>
      </header>
      <main>
        <div className="input-section">
          <label>
            Monthly Income:
            <input
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
            />
          </label>
        </div>
        <div className="expense-section">
          <div className="year-column">
            <h2>Year 1 Expenses</h2>
            {inflationCategories.map((category) => (
              <div key={category} className="expense-input">
                <label>
                  {category}:
                  <input
                    type="number"
                    value={year1[category]}
                    onChange={(e) =>
                      setYear1({ ...year1, [category]: e.target.value })
                    }
                  />
                </label>
              </div>
            ))}
          </div>
          <div className="year-column">
            <h2>Year 2 Expenses</h2>
            {inflationCategories.map((category) => (
              <div key={category} className="expense-input">
                <label>
                  {category}:
                  <input
                    type="number"
                    value={year2[category]}
                    onChange={(e) =>
                      setYear2({ ...year2, [category]: e.target.value })
                    }
                  />
                </label>
              </div>
            ))}
          </div>
        </div>
        <button onClick={handleCalculate}>Calculate</button>
        {results && (
          <div className="results-section">
            <h2>Results</h2>
            <p>Overall Inflation Rate: {results.overallInflation.toFixed(2)}%</p>
            <h3>Category Breakdown:</h3>
            <ul>
              {Object.entries(results.categoryBreakdown).map(
                ([category, data]) => (
                  <li key={category}>
                    {category}: {data.inflation.toFixed(2)}%
                  </li>
                )
              )}
            </ul>
            <button onClick={handleExport}>Export Data</button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

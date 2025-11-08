const express = require('express');
const app = express();
const port = 3001;

app.use(express.json());

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

// Placeholder for fetching historical inflation data
const getHistoricalInflation = async (category) => {
  // TODO: Replace this with a call to a real inflation data API
  // In a real application, this would fetch data from a reliable API
  // For now, we'll return a placeholder value
  console.log(`Fetching historical inflation for ${category}...`);
  return 2.5; // Placeholder inflation rate of 2.5%
};

app.post('/api/calculate', async (req, res) => {
  const { income, year1, year2 } = req.body;

  if (!income || !year1 || !year2) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  let totalYear1Expenses = 0;
  let totalYear2Expenses = 0;
  const categoryBreakdown = {};

  for (const category of inflationCategories) {
    const expenseYear1 = year1[category] || 0;
    const expenseYear2 = year2[category] || 0;

    totalYear1Expenses += expenseYear1;
    totalYear2Expenses += expenseYear2;

    if (expenseYear1 === 0 && expenseYear2 > 0) {
      // If there's no spending in the first year, use historical data
      const historicalInflation = await getHistoricalInflation(category);
      const estimatedYear1Expense = expenseYear2 / (1 + historicalInflation / 100);
      categoryBreakdown[category] = {
        inflation: historicalInflation,
        year1: estimatedYear1Expense,
        year2: expenseYear2,
      };
    } else if (expenseYear1 > 0) {
      const inflation = ((expenseYear2 - expenseYear1) / expenseYear1) * 100;
      categoryBreakdown[category] = {
        inflation: inflation,
        year1: expenseYear1,
        year2: expenseYear2,
      };
    } else {
      categoryBreakdown[category] = {
        inflation: 0,
        year1: 0,
        year2: 0,
      };
    }
  }

  const overallInflation =
    totalYear1Expenses > 0
      ? ((totalYear2Expenses - totalYear1Expenses) / totalYear1Expenses) * 100
      : 0;

  res.json({
    overallInflation,
    categoryBreakdown,
    income,
    totalYear1Expenses,
    totalYear2Expenses,
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

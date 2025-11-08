import { render, screen } from '@testing-library/react';
import App from './App';

test('renders personal inflation calculator heading', () => {
  render(<App />);
  const linkElement = screen.getByText(/Personal Inflation Calculator/i);
  expect(linkElement).toBeInTheDocument();
});

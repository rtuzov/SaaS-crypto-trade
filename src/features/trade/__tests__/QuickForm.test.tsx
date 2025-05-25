import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { QuickForm } from '../QuickForm';

// Mock fetch
const mockFetch = jest.fn();
globalThis.fetch = mockFetch;

describe('QuickForm', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders form fields correctly', () => {
    render(<QuickForm />);

    expect(screen.getByLabelText(/symbol/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/side/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/order type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/size/i)).toBeInTheDocument();
  });

  it('shows price field only for limit orders', () => {
    render(<QuickForm />);

    // Price field should not be visible initially (market order)
    expect(screen.queryByLabelText(/price/i)).not.toBeInTheDocument();

    // Change to limit order
    fireEvent.change(screen.getByLabelText(/order type/i), {
      target: { value: 'LIMIT' },
    });

    // Price field should now be visible
    expect(screen.getByLabelText(/price/i)).toBeInTheDocument();
  });

  it('submits form with correct data', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: '123' }),
    });

    render(<QuickForm />);

    // Fill form
    fireEvent.change(screen.getByLabelText(/symbol/i), {
      target: { value: 'BTC/USDT' },
    });
    fireEvent.click(screen.getByLabelText(/long/i));
    fireEvent.change(screen.getByLabelText(/size/i), {
      target: { value: '0.1' },
    });

    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /execute trade/i }));

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/execute_trade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: 'BTC/USDT',
          side: 'LONG',
          type: 'MARKET',
          size: 0.1,
        }),
      });
    });
  });

  it('shows loading state during submission', async () => {
    mockFetch.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 100)),
    );

    render(<QuickForm />);

    // Fill and submit form
    fireEvent.change(screen.getByLabelText(/size/i), {
      target: { value: '0.1' },
    });
    fireEvent.click(screen.getByRole('button', { name: /execute trade/i }));

    // Should show loading state
    expect(screen.getByRole('button', { name: /executing/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /executing/i })).toBeDisabled();
  });
});

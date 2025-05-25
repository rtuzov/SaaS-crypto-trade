import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { HistoryDrawer } from '../HistoryDrawer';

// Mock fetch
const mockFetch = jest.fn();
globalThis.fetch = mockFetch;

describe('HistoryDrawer', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders closed by default', () => {
    render(<HistoryDrawer />);

    expect(screen.queryByText(/Trade History/i)).not.toBeInTheDocument();
  });

  it('opens when button is clicked', () => {
    render(<HistoryDrawer />);
    fireEvent.click(screen.getByRole('button'));

    expect(screen.getByText(/Trade History/i)).toBeInTheDocument();
  });

  it('fetches and displays trade history', async () => {
    const mockTrades = [
      {
        id: '1',
        symbol: 'BTC/USDT',
        side: 'LONG',
        entry_price: 50000,
        exit_price: 51000,
        size: 0.1,
        pnl: 100,
        timestamp: Date.now(),
      },
    ];

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockTrades),
    });

    render(<HistoryDrawer />);
    fireEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(screen.getByText(/BTC\/USDT/i)).toBeInTheDocument();
      expect(screen.getByText(/LONG/i)).toBeInTheDocument();
      expect(screen.getByText(/50000.00/)).toBeInTheDocument();
      expect(screen.getByText(/51000.00/)).toBeInTheDocument();
      expect(screen.getByText(/0.1000/)).toBeInTheDocument();
      expect(screen.getAllByText(/100.00/).length).toBeGreaterThan(0);
    });
  });

  it('shows error state when fetch fails', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<HistoryDrawer />);
    fireEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(screen.getByText(/no trades/i)).toBeInTheDocument();
    });
  });

  it('closes when close button is clicked', async () => {
    render(<HistoryDrawer />);
    fireEvent.click(screen.getByRole('button'));

    expect(screen.getByText(/Trade History/i)).toBeInTheDocument();

    const closeButtons = screen.getAllByRole('button');
    const closeBtn = closeButtons[1];
    if (!closeBtn) {
      throw new Error('Close button not found');
    }
    fireEvent.click(closeBtn);
    await waitFor(() => {
      expect(screen.queryByText(/Trade History/i)).not.toBeInTheDocument();
    });
  });
});

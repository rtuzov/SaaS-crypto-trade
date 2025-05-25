import { render, screen, waitFor } from '@testing-library/react';

import { LatencyBadge } from '../LatencyBadge';

// Mock fetch
global.fetch = jest.fn();

describe('LatencyBadge', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('shows offline state initially', () => {
    render(<LatencyBadge />);

    expect(screen.getByText('Offline')).toBeInTheDocument();
  });

  it('shows latency when ping is successful', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ timestamp: Date.now() }),
    });

    render(<LatencyBadge />);

    await waitFor(() => {
      expect(screen.queryByText('Offline')).not.toBeInTheDocument();
    });

    expect(screen.getByText(/ms$/)).toBeInTheDocument();
  });

  it('shows error state when ping fails', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<LatencyBadge />);

    await waitFor(() => {
      expect(screen.getByText('Offline')).toBeInTheDocument();
    });
  });
});

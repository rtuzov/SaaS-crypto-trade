import { render, screen, waitFor } from '@testing-library/react';

import { SignalChat } from '../SignalChat';

// Mock WebSocket
class MockWebSocket {
  onopen: (() => void) | null = null;
  onmessage: ((event: { data: string }) => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: (() => void) | null = null;
  readyState = 0;

  constructor() {
    setTimeout(() => {
      if (this.onopen) {
        this.onopen();
      }
    }, 0);
  }

  send() {}
  close() {}
}

const mockWebSocket = jest.fn(() => new MockWebSocket());
globalThis.WebSocket = mockWebSocket as unknown as typeof WebSocket;

describe('SignalChat', () => {
  beforeEach(() => {
    mockWebSocket.mockClear();
  });

  it('shows connecting state initially', () => {
    render(<SignalChat />);

    expect(screen.getByText(/connecting/i)).toBeInTheDocument();
  });

  it('shows connected state after WebSocket connects', async () => {
    render(<SignalChat />);
    await waitFor(() => {
      expect(screen.getByText(/connected/i)).toBeInTheDocument();
    });
  });

  it('displays signals when received', async () => {
    render(<SignalChat />);

    const mockSignal = {
      id: '1',
      symbol: 'BTC/USDT',
      side: 'LONG',
      price: 50000,
      timestamp: Date.now(),
    };

    await waitFor(() => {
      const ws = mockWebSocket.mock.results[0].value;
      if (ws.onmessage) {
        ws.onmessage({ data: JSON.stringify(mockSignal) });
      }
    });

    expect(screen.getByText(/BTC\/USDT/i)).toBeInTheDocument();
    expect(screen.getByText(/LONG/i)).toBeInTheDocument();
    expect(screen.getByText(/50000/)).toBeInTheDocument();
  });

  it('shows empty state when no signals', () => {
    render(<SignalChat />);

    expect(screen.getByText(/no signals/i)).toBeInTheDocument();
  });
});

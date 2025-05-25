'use client';

import { useEffect, useState } from 'react';

type Trade = {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  entry_price: number;
  exit_price: number;
  size: number;
  pnl: number;
  timestamp: number;
};

export function HistoryDrawer() {
  const [isOpen, setIsOpen] = useState(false);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchTrades = async () => {
    try {
      const response = await fetch('/api/trade_history');
      if (!response.ok) {
        throw new Error('Failed to fetch trade history');
      }
      const data = await response.json();
      setTrades(data);
    } catch (error) {
      console.error('Error fetching trade history:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchTrades();
    }
  }, [isOpen]);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 rounded-full bg-blue-600 p-4 text-white shadow-lg hover:bg-blue-700"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="size-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          <div
            className="absolute inset-0 bg-black bg-opacity-50"
            onClick={() => setIsOpen(false)}
            onKeyDown={e => e.key === 'Escape' && setIsOpen(false)}
            role="button"
            tabIndex={0}
          />
          <div className="absolute right-0 top-0 h-full w-96 bg-white shadow-xl">
            <div className="flex h-16 items-center justify-between border-b px-4">
              <h2 className="text-lg font-semibold">Trade History</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="rounded-full p-2 hover:bg-gray-100"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="size-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <div className="h-[calc(100%-4rem)] overflow-y-auto p-4">
              {loading
                ? (
                    <div className="flex h-full items-center justify-center">
                      <div className="size-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
                    </div>
                  )
                : trades.length === 0
                  ? (
                      <div className="flex h-full items-center justify-center text-gray-500">
                        No trades yet
                      </div>
                    )
                  : (
                      <div className="space-y-4">
                        {trades.map(trade => (
                          <div
                            key={trade.id}
                            className="rounded-lg border p-4 shadow-sm"
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-medium">{trade.symbol}</span>
                              <span
                                className={`font-medium ${
                                  trade.side === 'LONG' ? 'text-green-600' : 'text-red-600'
                                }`}
                              >
                                {trade.side}
                              </span>
                            </div>
                            <div className="mt-2 grid grid-cols-2 gap-2 text-sm text-gray-600">
                              <div>
                                <span className="font-medium">Entry:</span>
                                {' '}
                                {trade.entry_price.toFixed(2)}
                              </div>
                              <div>
                                <span className="font-medium">Exit:</span>
                                {' '}
                                {trade.exit_price.toFixed(2)}
                              </div>
                              <div>
                                <span className="font-medium">Size:</span>
                                {' '}
                                {trade.size.toFixed(4)}
                              </div>
                              <div>
                                <span className="font-medium">PnL:</span>
                                {' '}
                                <span
                                  className={
                                    trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                                  }
                                >
                                  {trade.pnl.toFixed(2)}
                                </span>
                              </div>
                            </div>
                            <div className="mt-2 text-xs text-gray-500">
                              {new Date(trade.timestamp).toLocaleString()}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

'use client';

import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';

type Trade = {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  entry_price: number;
  current_price: number;
  size: number;
  pnl: number;
  timestamp: number;
};

export function ActiveTrades() {
  const t = useTranslations('Trade');
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTrades = async () => {
    try {
      const response = await fetch('/api/active_trades');
      if (!response.ok) {
        throw new Error('Failed to fetch trades');
      }
      const data = await response.json();
      setTrades(data);
      setError(null);
    } catch (error) {
      console.error('Error fetching trades:', error);
      setError('Failed to load trades');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrades();
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  const closeTrade = async (tradeId: string) => {
    try {
      setError(null);
      const response = await fetch('/api/close_trade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tradeId }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to close trade');
      }

      setTrades(data.trades);
    } catch (error) {
      console.error('Error closing trade:', error);
      setError(error instanceof Error ? error.message : 'Failed to close trade');
    }
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="size-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-full items-center justify-center text-red-600">
        {error}
      </div>
    );
  }

  if (trades.length === 0) {
    return (
      <div className="flex h-full items-center justify-center text-gray-500">
        {t('no_active_trades')}
      </div>
    );
  }

  return (
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
              <span className="font-medium">Current:</span>
              {' '}
              {trade.current_price.toFixed(2)}
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
          <div className="mt-4 flex justify-end">
            <button
              onClick={() => closeTrade(trade.id)}
              className="rounded-md bg-red-600 px-4 py-2 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
            >
              {t('close_trade')}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

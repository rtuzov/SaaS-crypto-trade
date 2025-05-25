'use client';

import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

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

export default function RecentTransactions() {
  const t = useTranslations('Dashboard');
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
    fetchTrades();
    // Обновляем каждые 5 секунд
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="text-gray-900">{t('recentTransactions')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-32 items-center justify-center">
            <div className="size-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (trades.length === 0) {
    return (
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="text-gray-900">{t('recentTransactions')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-gray-600">
            {t('noTransactions')}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="text-gray-900">{t('recentTransactions')}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {trades.map(trade => (
            <div key={trade.id} className="rounded-lg border border-gray-200 bg-white p-3">
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">{trade.symbol}</span>
                <span className={`font-medium ${trade.side === 'LONG' ? 'text-green-600' : 'text-red-600'}`}>
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
                  <span className={trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'}>
                    {trade.pnl.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

'use client';

import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

type PnLData = {
  timestamp: number;
  value: number;
};

export default function PnlChart() {
  const t = useTranslations('Dashboard');
  const [data, setData] = useState<PnLData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPnL = async () => {
      try {
        const response = await fetch('/api/pnl');
        if (!response.ok) {
          throw new Error('Failed to fetch PnL data');
        }
        const pnlData = await response.json();
        setData(pnlData);
      } catch (error) {
        console.error('Error fetching PnL data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPnL();
  }, []);

  if (loading) {
    return (
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="text-gray-900">{t('pnl_chart')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-32 items-center justify-center">
            <div className="size-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (data.length === 0) {
    return (
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="text-gray-900">{t('pnl_chart')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-gray-600">
            {t('no_pnl_data')}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="text-gray-900">{t('pnl_chart')}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={timestamp => new Date(timestamp).toLocaleDateString()}
                stroke="#6b7280"
              />
              <YAxis stroke="#6b7280" />
              <Tooltip
                labelFormatter={timestamp => new Date(timestamp).toLocaleDateString()}
                formatter={(value: number) => [`$${value.toFixed(2)}`, 'PnL']}
                contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb' }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#2563eb"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

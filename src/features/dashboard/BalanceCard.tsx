'use client';

import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

type Balance = {
  total: number;
  available: number;
  locked: number;
};

export default function BalanceCard() {
  const t = useTranslations('Dashboard');
  const [balance, setBalance] = useState<Balance | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await fetch('/api/balance');
        if (!response.ok) {
          throw new Error('Failed to fetch balance');
        }
        const data = await response.json();
        setBalance(data);
      } catch (error) {
        console.error('Error fetching balance:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBalance();
  }, []);

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{t('total_balance')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-32 items-center justify-center">
            <div className="size-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!balance) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{t('total_balance')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-destructive">{t('balance.login_to_view')}</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('total_balance')}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4">
          <div>
            <div className="text-sm text-muted-foreground">{t('available_balance')}</div>
            <div className="text-2xl font-bold">
              ${balance.available.toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-sm text-muted-foreground">{t('in_trades')}</div>
            <div className="text-2xl font-bold">
              ${balance.locked.toFixed(2)}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

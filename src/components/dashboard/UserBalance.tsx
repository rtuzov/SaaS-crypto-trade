'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Icons } from '@/components/ui/icons';
import { useToast } from '@/components/ui/use-toast';
import { useTranslations } from 'next-intl';

interface BalanceData {
  total: number;
  available: number;
  locked: number;
}

export function UserBalance() {
  const { data: session } = useSession();
  const { toast } = useToast();
  const t = useTranslations('Dashboard.balance');
  const [balance, setBalance] = useState<BalanceData | null>(null);
  const [depositAmount, setDepositAmount] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingBalance, setIsLoadingBalance] = useState(true);
  
  // Загрузка баланса при монтировании компонента
  useEffect(() => {
    fetchBalance();
    
    // Обновление баланса каждые 30 секунд
    const interval = setInterval(fetchBalance, 30000);
    return () => clearInterval(interval);
  }, []);
  
  // Функция для получения баланса с API
  const fetchBalance = async () => {
    if (!session?.user) return;
    
    setIsLoadingBalance(true);
    try {
      const response = await fetch('/api/balance');
      
      if (!response.ok) {
        throw new Error('Ошибка при получении баланса');
      }
      
      const data = await response.json();
      setBalance(data);
    } catch (error) {
      console.error('Ошибка при загрузке баланса:', error);
      toast({
        title: 'Ошибка',
        description: 'Не удалось загрузить баланс. Попробуйте позже.',
        variant: 'destructive',
      });
    } finally {
      setIsLoadingBalance(false);
    }
  };
  
  // Функция для пополнения баланса
  const handleDeposit = async () => {
    if (!depositAmount || isNaN(Number(depositAmount)) || Number(depositAmount) <= 0) {
      toast({
        title: 'Ошибка',
        description: 'Пожалуйста, введите корректную сумму',
        variant: 'destructive',
      });
      return;
    }
    
    setIsLoading(true);
    try {
      const amount = Number(depositAmount);
      
      // В реальном приложении здесь будет запрос к API
      const response = await fetch('/api/balance/deposit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount }),
      });
      
      if (!response.ok) {
        throw new Error('Ошибка при пополнении баланса');
      }
      
      const result = await response.json();
      
      // Обновляем баланс
      setBalance(result);
      setDepositAmount('');
      
      toast({
        title: 'Успех',
        description: `Баланс успешно пополнен на $${amount.toFixed(2)}`,
      });
    } catch (error) {
      console.error('Ошибка при пополнении баланса:', error);
      toast({
        title: 'Ошибка',
        description: 'Не удалось пополнить баланс. Попробуйте позже.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!session?.user) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{t('title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{t('login_to_view')}</p>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {isLoadingBalance ? (
          <div className="space-y-2">
            <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-6 bg-gray-200 rounded w-3/4 animate-pulse"></div>
          </div>
        ) : (
          <>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">{t('total')}</span>
                <span className="font-bold">${balance?.total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">{t('available')}</span>
                <span className="font-medium">${balance?.available.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">{t('locked')}</span>
                <span className="font-medium">${balance?.locked.toFixed(2)}</span>
              </div>
            </div>
            
            <div className="pt-4 border-t">
              <div className="space-y-2">
                <Label htmlFor="amount">{t('deposit_amount')}</Label>
                <div className="flex space-x-2">
                  <Input
                    id="amount"
                    type="number"
                    min="1"
                    placeholder="100"
                    value={depositAmount}
                    onChange={(e) => setDepositAmount(e.target.value)}
                    disabled={isLoading}
                  />
                  <Button onClick={handleDeposit} disabled={isLoading}>
                    {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
                    {t('deposit_button')}
                  </Button>
                </div>
              </div>
            </div>
          </>
        )}
      </CardContent>
      <CardFooter>
        <p className="text-xs text-muted-foreground">
          {t('deposit_min')}
        </p>
      </CardFooter>
    </Card>
  );
} 
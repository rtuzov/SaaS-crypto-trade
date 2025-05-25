'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Icons } from '@/components/ui/icons';
import { useToast } from '@/components/ui/use-toast';

interface Transaction {
  id: string;
  type: 'deposit' | 'withdrawal' | 'trade';
  amount: number;
  status: 'completed' | 'pending' | 'failed';
  date: string;
  description: string;
}

export function TransactionHistory() {
  const { data: session } = useSession();
  const { toast } = useToast();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    fetchTransactions();
  }, []);
  
  const fetchTransactions = async () => {
    if (!session?.user) return;
    
    setIsLoading(true);
    try {
      // В реальном приложении здесь будет запрос к API
      // Имитация загрузки данных
      setTimeout(() => {
        const mockTransactions: Transaction[] = [
          {
            id: '1',
            type: 'deposit',
            amount: 1000,
            status: 'completed',
            date: new Date().toISOString(),
            description: 'Пополнение счета',
          },
          {
            id: '2',
            type: 'trade',
            amount: -250,
            status: 'completed',
            date: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
            description: 'Открытие позиции BTC/USDT',
          },
          {
            id: '3',
            type: 'trade',
            amount: 320,
            status: 'completed',
            date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Закрытие позиции ETH/USDT',
          },
          {
            id: '4',
            type: 'withdrawal',
            amount: -500,
            status: 'pending',
            date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Вывод средств',
          },
        ];
        
        setTransactions(mockTransactions);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Ошибка при загрузке транзакций:', error);
      toast({
        title: 'Ошибка',
        description: 'Не удалось загрузить историю транзакций. Попробуйте позже.',
        variant: 'destructive',
      });
      setIsLoading(false);
    }
  };
  
  // Функция для форматирования даты
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };
  
  // Функция для определения цвета статуса
  const getStatusBadge = (status: Transaction['status']) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-800 border-green-200">Выполнено</Badge>;
      case 'pending':
        return <Badge className="bg-yellow-100 text-yellow-800 border-yellow-200">В обработке</Badge>;
      case 'failed':
        return <Badge className="bg-red-100 text-red-800 border-red-200">Ошибка</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };
  
  if (!session?.user) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>История транзакций</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Пожалуйста, авторизуйтесь для просмотра истории транзакций</p>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>История транзакций</CardTitle>
        <CardDescription>
          Просмотр всех операций по вашему счету
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-2">
            <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
          </div>
        ) : transactions.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground">У вас пока нет транзакций</p>
            <Button 
              variant="outline" 
              className="mt-4"
              onClick={() => window.location.href = '/dashboard'}
            >
              Вернуться в личный кабинет
            </Button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Дата</TableHead>
                  <TableHead>Тип</TableHead>
                  <TableHead>Описание</TableHead>
                  <TableHead className="text-right">Сумма</TableHead>
                  <TableHead>Статус</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.map((transaction) => (
                  <TableRow key={transaction.id}>
                    <TableCell className="font-medium">
                      {formatDate(transaction.date)}
                    </TableCell>
                    <TableCell>
                      {transaction.type === 'deposit' && 'Пополнение'}
                      {transaction.type === 'withdrawal' && 'Вывод'}
                      {transaction.type === 'trade' && 'Трейдинг'}
                    </TableCell>
                    <TableCell>{transaction.description}</TableCell>
                    <TableCell className={`text-right ${transaction.amount >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {transaction.amount >= 0 ? '+' : ''}${transaction.amount.toFixed(2)}
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(transaction.status)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
} 
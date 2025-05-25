import { Metadata } from 'next';
import { TransactionHistory } from '@/components/dashboard/TransactionHistory';

export const metadata: Metadata = {
  title: 'История транзакций',
  description: 'Просмотр истории транзакций пользователя',
};

export default function TransactionsPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">История транзакций</h1>
      
      <TransactionHistory />
    </main>
  );
} 
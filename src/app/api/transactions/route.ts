import { NextResponse } from 'next/server';

export async function GET() {
  // TODO: Заменить на реальные данные из базы данных
  const mockTransactions = [
    {
      id: '1',
      type: 'DEPOSIT',
      amount: 5000,
      status: 'COMPLETED',
      timestamp: new Date('2024-01-01').getTime(),
    },
    {
      id: '2',
      type: 'TRADE',
      amount: 1000,
      status: 'COMPLETED',
      timestamp: new Date('2024-01-02').getTime(),
    },
    {
      id: '3',
      type: 'WITHDRAWAL',
      amount: 2000,
      status: 'PENDING',
      timestamp: new Date('2024-01-03').getTime(),
    },
  ];

  return NextResponse.json(mockTransactions);
}

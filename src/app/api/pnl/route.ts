import { NextResponse } from 'next/server';

export async function GET() {
  // TODO: Заменить на реальные данные из базы данных
  const mockPnLData = [
    { date: '2024-01-01', pnl: 0 },
    { date: '2024-01-02', pnl: 100 },
    { date: '2024-01-03', pnl: -50 },
    { date: '2024-01-04', pnl: 200 },
    { date: '2024-01-05', pnl: 150 },
    { date: '2024-01-06', pnl: 300 },
    { date: '2024-01-07', pnl: 250 },
  ];

  return NextResponse.json(mockPnLData);
}

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

import { activeTradesStore } from '@/libs/store/activeTrades';
import { authOptions } from '@/libs/auth';

export async function POST(request: Request) {
  try {
    const session = await getServerSession(authOptions);
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { tradeId } = body;

    if (!tradeId) {
      return NextResponse.json({ error: 'Trade ID is required' }, { status: 400 });
    }

    const success = activeTradesStore.closeTrade(tradeId);

    if (!success) {
      return NextResponse.json({ error: 'Trade not found' }, { status: 404 });
    }

    // Возвращаем обновленный список активных сделок
    const updatedTrades = activeTradesStore.getTrades();
    return NextResponse.json({ success: true, trades: updatedTrades });
  } catch (error) {
    console.error('Error closing trade:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

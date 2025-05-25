// active_trades/route.ts
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/libs/auth';
import { activeTradesStore } from '@/libs/store/activeTrades';

export async function GET() {
  try {
    const session = await getServerSession();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const trades = activeTradesStore.getTrades();
    return NextResponse.json(trades);
  } catch (error) {
    console.error('Error fetching active trades:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

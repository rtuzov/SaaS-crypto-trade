import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

import { activeTradesStore } from '@/libs/store/activeTrades';
import { authOptions } from '@/libs/auth';

export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    const closedTrades = activeTradesStore.getClosedTrades();
    console.log('Closed trades from store:', closedTrades);
    return NextResponse.json(closedTrades);
  } catch (error) {
    console.error('Error fetching trade history:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

export async function DELETE() {
  try {
    const session = await getServerSession(authOptions);
    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    activeTradesStore.clearHistory();
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error clearing trade history:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

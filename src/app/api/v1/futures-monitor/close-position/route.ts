import { NextResponse } from 'next/server';
import { BinanceClient } from '@/libs/binance';

export async function POST(request: Request) {
  const apiKey = request.headers.get('X-API-Key');
  const apiSecret = request.headers.get('X-API-Secret');

  if (!apiKey || !apiSecret) {
    return NextResponse.json(
      { error: 'API credentials are required' },
      { status: 401 }
    );
  }

  try {
    const { symbol, side } = await request.json();
    
    if (!symbol || !side) {
      return NextResponse.json(
        { error: 'Symbol and side are required' },
        { status: 400 }
      );
    }

    const client = new BinanceClient(apiKey, apiSecret);
    await client.closePosition(symbol, side);
    
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error closing position:', error);
    return NextResponse.json(
      { error: 'Failed to close position' },
      { status: 500 }
    );
  }
} 
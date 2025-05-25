import { NextResponse } from 'next/server';
import { BinanceClient } from '@/libs/binance';

export async function GET(request: Request) {
  const apiKey = request.headers.get('X-API-Key');
  const apiSecret = request.headers.get('X-API-Secret');

  if (!apiKey || !apiSecret) {
    return NextResponse.json(
      { error: 'API credentials are required' },
      { status: 401 }
    );
  }

  try {
    const client = new BinanceClient(apiKey, apiSecret);
    const positions = await client.getPositions();
    
    return NextResponse.json(positions);
  } catch (error) {
    console.error('Error fetching positions:', error);
    return NextResponse.json(
      { error: 'Failed to fetch positions' },
      { status: 500 }
    );
  }
} 
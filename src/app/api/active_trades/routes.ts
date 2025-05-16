// active_trades/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json([
    { pair: 'BTCUSDT', side: 'Long', size: 0.1, risk: 12 },
    { pair: 'ETHUSDT', side: 'Short', size: 2, risk: 55 },
  ]);
}

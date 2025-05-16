// balance/route.ts
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

import { authOptions } from '../auth/[...nextauth]/route';

export async function GET() {
  try {
    const session = await getServerSession(authOptions);

    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    // TODO: Replace with actual balance fetching logic
    const balance = {
      total: 10000.00,
      available: 7500.00,
      in_trades: 2500.00,
    };

    return NextResponse.json(balance);
  } catch (error) {
    console.error('Error fetching balance:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

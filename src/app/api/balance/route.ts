// balance/route.ts
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

import { authOptions } from '@/libs/auth';

export async function GET() {
  try {
    const session = await getServerSession(authOptions);

    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    // TODO: Заменить на реальные данные из базы данных
    const mockBalance = {
      total: 10000.00,
      available: 8000.00,
      locked: 2000.00,
    };

    return NextResponse.json(mockBalance);
  } catch (error) {
    console.error('Error fetching balance:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

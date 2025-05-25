import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { cmd } = await req.json();
  console.log('EXECUTE_TRADE', cmd);
  return NextResponse.json({ msg: 'queued', cmd });
}

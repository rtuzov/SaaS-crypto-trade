// import { Buffer } from 'node:buffer';

import { WebSocketServer } from 'ws';

export const runtime = 'edge';

export async function GET(req: Request) {
  // @ts-ignore — Deno specific API available in Edge runtime
  const { socket, response } = (globalThis as any).Deno.upgradeWebSocket(req);
  socket.onmessage = (e: MessageEvent) => socket.send(`echo:${e.data}`);
  return response;
}

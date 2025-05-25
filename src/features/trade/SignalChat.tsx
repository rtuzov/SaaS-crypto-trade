'use client';

import { useEffect, useState } from 'react';

type Signal = {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  price: number;
  timestamp: number;
};

export function SignalChat() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Mock WebSocket connection
    const ws = new WebSocket('ws://localhost:3000/api/ws/trade');

    ws.onopen = () => {
      setConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const signal = JSON.parse(event.data);
      setSignals(prev => [...prev, signal]);
    };

    ws.onclose = () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="h-[400px] overflow-y-auto rounded-lg border bg-gray-50 p-4">
      {!connected && (
        <div className="mb-4 rounded bg-yellow-100 p-2 text-yellow-800">
          Connecting to signal feed...
        </div>
      )}
      <div className="space-y-2">
        {signals.map(signal => (
          <div
            key={signal.id}
            className={`rounded p-2 ${
              signal.side === 'LONG' ? 'bg-green-100' : 'bg-red-100'
            }`}
          >
            <div className="flex justify-between">
              <span className="font-medium">{signal.symbol}</span>
              <span className={signal.side === 'LONG' ? 'text-green-600' : 'text-red-600'}>
                {signal.side}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              Price: $
              {signal.price.toFixed(2)}
            </div>
            <div className="text-xs text-gray-500">
              {new Date(signal.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {signals.length === 0 && (
          <div className="text-center text-gray-500">No signals yet</div>
        )}
      </div>
    </div>
  );
}

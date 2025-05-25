type Signal = {
  symbol: string;
  side: 'LONG' | 'SHORT';
  entry_price: number;
  stop_loss?: number;
  take_profit?: number;
};

export function parseSignal(text: string): Signal | null {
  // Пример формата: BTC/USDT LONG @ 50000 SL: 49000 TP: 52000
  const regex = /(\w+\/\w+)\s+(LONG|SHORT)\s+@\s+(\d+)(?:\s+SL:\s+(\d+))?(?:\s+TP:\s+(\d+))?/i;
  const match = text.match(regex);

  if (!match) {
    return null;
  }

  const [, symbol, side, entryPrice, stopLoss, takeProfit] = match;

  if (!symbol || !side || !entryPrice) {
    return null;
  }

  return {
    symbol: symbol.toUpperCase(),
    side: side.toUpperCase() as 'LONG' | 'SHORT',
    entry_price: Number.parseFloat(entryPrice),
    stop_loss: stopLoss ? Number.parseFloat(stopLoss) : undefined,
    take_profit: takeProfit ? Number.parseFloat(takeProfit) : undefined,
  };
}

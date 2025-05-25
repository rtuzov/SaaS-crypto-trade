export type Trade = {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  entry_price: number;
  current_price: number;
  exit_price?: number;
  size: number;
  pnl: number;
  timestamp: number;
};

// Серверное хранилище сделок
let trades: Trade[] = [];
let closedTrades: Trade[] = [];

export const activeTradesStore = {
  getTrades: () => {
    return trades;
  },
  getClosedTrades: () => {
    return closedTrades;
  },
  addTrade: (trade: Omit<Trade, 'id' | 'timestamp'>) => {
    const newTrade: Trade = {
      ...trade,
      id: Math.random().toString(36).substring(7),
      timestamp: Date.now(),
    };
    trades.push(newTrade);
    return newTrade;
  },
  closeTrade: (tradeId: string) => {
    const tradeIndex = trades.findIndex(t => t.id === tradeId);
    if (tradeIndex === -1) {
      return false;
    }

    const trade = trades[tradeIndex];
    if (!trade) {
      return false;
    }

    // Закрываем только выбранную сделку
    const closedTrade: Trade = {
      ...trade,
      exit_price: trade.current_price,
    };

    closedTrades.push(closedTrade);
    trades = trades.filter(t => t.id !== tradeId);
    return true;
  },
  clearHistory: () => {
    closedTrades = [];
  },
};

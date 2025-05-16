'use client';

import { useQuery } from 'urql';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const ACTIVE_TRADES_QUERY = `
  query ActiveTrades($traderId: ID!) {
    active_trades(trader_id: $traderId) {
      id
      symbol
      side
      entry_price
      current_price
      size
      pnl
      timestamp
    }
  }
`;

type Trade = {
  id: string;
  symbol: string;
  side: 'LONG' | 'SHORT';
  entry_price: number;
  current_price: number;
  size: number;
  pnl: number;
  timestamp: number;
};

export function ActiveTradesTable({ traderId }: { traderId: string }) {
  const [result] = useQuery({
    query: ACTIVE_TRADES_QUERY,
    variables: { traderId },
  });

  const { data, fetching, error } = result;

  if (fetching) {
    return (
      <div className="animate-pulse">
        <div className="mb-4 h-8 rounded bg-gray-200"></div>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 rounded bg-gray-200"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500">
        Error:
        {error.message}
      </div>
    );
  }

  const trades: Trade[] = data?.active_trades || [];

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Symbol</TableHead>
            <TableHead>Side</TableHead>
            <TableHead>Entry Price</TableHead>
            <TableHead>Current Price</TableHead>
            <TableHead>Size</TableHead>
            <TableHead>PnL</TableHead>
            <TableHead>Time</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {trades.map(trade => (
            <TableRow key={trade.id}>
              <TableCell>{trade.symbol}</TableCell>
              <TableCell>
                <span
                  className={
                    trade.side === 'LONG'
                      ? 'text-green-500'
                      : 'text-red-500'
                  }
                >
                  {trade.side}
                </span>
              </TableCell>
              <TableCell>
                $
                {trade.entry_price.toFixed(2)}
              </TableCell>
              <TableCell>
                $
                {trade.current_price.toFixed(2)}
              </TableCell>
              <TableCell>{trade.size}</TableCell>
              <TableCell
                className={
                  trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'
                }
              >
                $
                {trade.pnl.toFixed(2)}
              </TableCell>
              <TableCell>
                {new Date(trade.timestamp).toLocaleTimeString()}
              </TableCell>
            </TableRow>
          ))}
          {trades.length === 0 && (
            <TableRow>
              <TableCell colSpan={7} className="text-center">
                No active trades
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'

const trades = [
  {
    pair: 'BTC/USDT',
    side: 'long',
    size: '0.1 BTC',
    entry: '$45,000',
    pnl: '+2.5%',
    tp: '$46,000',
    sl: '$44,000'
  },
  {
    pair: 'ETH/USDT',
    side: 'short',
    size: '1 ETH',
    entry: '$3,000',
    pnl: '-1.2%',
    tp: '$2,900',
    sl: '$3,100'
  }
]

export function ActiveTrades() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Активные сделки</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Пара</TableHead>
              <TableHead>Сторона</TableHead>
              <TableHead>Размер</TableHead>
              <TableHead>Вход</TableHead>
              <TableHead>PnL</TableHead>
              <TableHead>TP</TableHead>
              <TableHead>SL</TableHead>
              <TableHead>Действия</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {trades.map((trade) => (
              <TableRow key={trade.pair}>
                <TableCell>{trade.pair}</TableCell>
                <TableCell>
                  <Badge variant={trade.side === 'long' ? 'default' : 'destructive'}>
                    {trade.side === 'long' ? 'Long' : 'Short'}
                  </Badge>
                </TableCell>
                <TableCell>{trade.size}</TableCell>
                <TableCell>{trade.entry}</TableCell>
                <TableCell className={trade.pnl.startsWith('+') ? 'text-green-500' : 'text-red-500'}>
                  {trade.pnl}
                </TableCell>
                <TableCell>{trade.tp}</TableCell>
                <TableCell>{trade.sl}</TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Button variant="outline" size="sm">
                      Close
                    </Button>
                    <Button variant="outline" size="sm">
                      TP
                    </Button>
                    <Button variant="outline" size="sm">
                      SL
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
} 
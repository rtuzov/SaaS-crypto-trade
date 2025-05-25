import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'

const trades = [
  {
    id: 1,
    pair: 'BTC/USDT',
    side: 'long',
    size: '0.1 BTC',
    entry: '$45,000',
    exit: '$46,000',
    pnl: '+$100',
    timestamp: '10:30:15'
  },
  {
    id: 2,
    pair: 'ETH/USDT',
    side: 'short',
    size: '1 ETH',
    entry: '$3,000',
    exit: '$2,900',
    pnl: '+$100',
    timestamp: '10:35:20'
  }
]

export function TradeHistory() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>История сделок</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px]">
          <div className="space-y-4">
            {trades.map((trade) => (
              <div
                key={trade.id}
                className="p-4 bg-muted rounded-lg"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <Badge variant={trade.side === 'long' ? 'default' : 'destructive'}>
                      {trade.side === 'long' ? 'Long' : 'Short'}
                    </Badge>
                    <span className="ml-2 font-medium">{trade.pair}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {trade.timestamp}
                  </span>
                </div>
                
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-muted-foreground">Размер:</span>
                    <span className="ml-2">{trade.size}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Вход:</span>
                    <span className="ml-2">{trade.entry}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Выход:</span>
                    <span className="ml-2">{trade.exit}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">PnL:</span>
                    <span className="ml-2 text-green-500">{trade.pnl}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
} 
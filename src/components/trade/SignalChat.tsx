'use client';
import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Send } from 'lucide-react'

const messages = [
  {
    id: 1,
    text: 'BTC/USDT Long 0.1 BTC @ $45,000 TP: $46,000 SL: $44,000',
    timestamp: '10:30:15',
    type: 'signal'
  },
  {
    id: 2,
    text: 'Order executed: BTC/USDT Long 0.1 BTC @ $45,000',
    timestamp: '10:30:16',
    type: 'execution'
  },
  {
    id: 3,
    text: 'ETH/USDT Short 1 ETH @ $3,000 TP: $2,900 SL: $3,100',
    timestamp: '10:35:20',
    type: 'signal'
  }
]

export function SignalChat() {
  const [message, setMessage] = useState('')
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement message sending
    setMessage('')
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Сигналы</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[400px] overflow-y-auto mb-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`p-3 rounded-lg ${
                msg.type === 'signal'
                  ? 'bg-primary/10'
                  : 'bg-muted'
              }`}
            >
              <div className="flex justify-between text-sm text-muted-foreground mb-1">
                <span>{msg.type === 'signal' ? 'Сигнал' : 'Исполнение'}</span>
                <span>{msg.timestamp}</span>
              </div>
              <p>{msg.text}</p>
            </div>
          ))}
        </div>
        
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Textarea
            value={message}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setMessage(e.target.value)}
            placeholder="Введите команду..."
            className="min-h-[60px]"
          />
          <Button type="submit" size="sm" className="self-end">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  )
} 
'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export function TradeForm() {
  const [side, setSide] = useState<'long' | 'short'>('long');
  const [amount, setAmount] = useState('');
  const [leverage, setLeverage] = useState('1');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement trade execution
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Новая сделка</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Button
              type="button"
              variant={side === 'long' ? 'default' : 'outline'}
              onClick={() => setSide('long')}
            >
              Long
            </Button>
            <Button
              type="button"
              variant={side === 'short' ? 'primary' : 'outline'}
              onClick={() => setSide('short')}
            >
              Short
            </Button>
          </div>

          <div className="space-y-2">
            <Label htmlFor="amount">Количество (USDT)</Label>
            <Input
              id="amount"
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="leverage">Кредитное плечо</Label>
            <Select value={leverage} onValueChange={setLeverage}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {[1, 2, 5, 10, 20, 50, 100].map((value) => (
                  <SelectItem key={value} value={value.toString()}>
                    {value}x
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button type="submit" className="w-full">
            Открыть позицию
          </Button>
        </form>
      </CardContent>
    </Card>
  );
} 
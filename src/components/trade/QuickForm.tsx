'use client';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from 'react';

export function QuickForm() {
  const [command, setCommand] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: интеграция с backend для быстрой команды
    setCommand('');
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick command</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="btc long 0.05 5x tp 70000 sl 64000"
          />
          <Button type="submit">Send</Button>
        </form>
      </CardContent>
    </Card>
  );
} 
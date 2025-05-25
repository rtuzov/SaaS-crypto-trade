'use client';

import { useState } from 'react';

type OrderType = 'MARKET' | 'LIMIT';

export function QuickForm() {
  const [symbol, setSymbol] = useState('BTC/USDT');
  const [side, setSide] = useState<'LONG' | 'SHORT'>('LONG');
  const [type, setType] = useState<OrderType>('MARKET');
  const [price, setPrice] = useState('');
  const [size, setSize] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('/api/execute_trade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol,
          side,
          type,
          price: type === 'LIMIT' ? Number.parseFloat(price) : undefined,
          size: Number.parseFloat(size),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to execute trade');
      }

      // Reset form
      setPrice('');
      setSize('');
    } catch (error) {
      console.error('Error executing trade:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Symbol</label>
        <select
          value={symbol}
          onChange={e => setSymbol(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="BTC/USDT">BTC/USDT</option>
          <option value="ETH/USDT">ETH/USDT</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Side</label>
        <div className="mt-1 flex space-x-4">
          <label className="inline-flex items-center">
            <input
              type="radio"
              value="LONG"
              checked={side === 'LONG'}
              onChange={e => setSide(e.target.value as 'LONG')}
              className="size-4 text-blue-600"
            />
            <span className="ml-2 text-green-600">LONG</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              value="SHORT"
              checked={side === 'SHORT'}
              onChange={e => setSide(e.target.value as 'SHORT')}
              className="size-4 text-blue-600"
            />
            <span className="ml-2 text-red-600">SHORT</span>
          </label>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Order Type</label>
        <select
          value={type}
          onChange={e => setType(e.target.value as OrderType)}
          className="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="MARKET">Market</option>
          <option value="LIMIT">Limit</option>
        </select>
      </div>

      {type === 'LIMIT' && (
        <div>
          <label className="block text-sm font-medium text-gray-700">Price</label>
          <input
            type="number"
            value={price}
            onChange={e => setPrice(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="0.00"
            step="0.01"
            required
          />
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700">Size</label>
        <input
          type="number"
          value={size}
          onChange={e => setSize(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          placeholder="0.00"
          step="0.01"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
      >
        {loading ? 'Executing...' : 'Execute Trade'}
      </button>
    </form>
  );
}

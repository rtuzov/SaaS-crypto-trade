'use client';

import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';
import { useState } from 'react';

type TradeCommand = {
  symbol: string;
  side: 'LONG' | 'SHORT';
  size: number;
};

export function TradeTerminal() {
  const { data: session } = useSession();
  const t = useTranslations('Trade');
  const [command, setCommand] = useState<TradeCommand>({
    symbol: 'BTC/USDT',
    side: 'LONG',
    size: 1,
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) {
      setError('Unauthorized');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/execute_trade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(command),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to execute trade');
      }

      // Reset form
      setCommand({
        symbol: 'BTC/USDT',
        side: 'LONG',
        size: 1,
      });
    } catch (error) {
      console.error('Trade error:', error);
      setError(error instanceof Error ? error.message : 'Failed to execute trade');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl rounded-lg bg-white p-8 shadow-lg">
      <h2 className="mb-6 text-2xl font-semibold text-gray-900">{t('terminal_title')}</h2>

      {error && (
        <div className="mb-4 rounded bg-red-100 p-4 text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            {t('symbol')}
          </label>
          <input
            type="text"
            value={command.symbol}
            onChange={e => setCommand({ ...command, symbol: e.target.value })}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            {t('side')}
          </label>
          <select
            value={command.side}
            onChange={e => setCommand({ ...command, side: e.target.value as 'LONG' | 'SHORT' })}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
            required
          >
            <option value="LONG">{t('long')}</option>
            <option value="SHORT">{t('short')}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            {t('size')}
          </label>
          <input
            type="number"
            min="0.01"
            step="0.01"
            value={command.size}
            onChange={e => setCommand({ ...command, size: Number.parseFloat(e.target.value) })}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? t('executing') : t('execute')}
        </button>
      </form>
    </div>
  );
}

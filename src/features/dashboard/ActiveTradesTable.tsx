'use client';

import { useTranslations } from 'next-intl';

export default function ActiveTradesTable() {
  const t = useTranslations('Dashboard');

  return (
    <div className="rounded-lg bg-white p-6 shadow-md">
      <h2 className="mb-4 text-xl font-semibold">{t('active_trades')}</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="px-4 py-2 text-left">{t('symbol')}</th>
              <th className="px-4 py-2 text-left">{t('side')}</th>
              <th className="px-4 py-2 text-left">{t('entry_price')}</th>
              <th className="px-4 py-2 text-left">{t('current_price')}</th>
              <th className="px-4 py-2 text-left">{t('size')}</th>
              <th className="px-4 py-2 text-left">{t('pnl')}</th>
              <th className="px-4 py-2 text-left">{t('time')}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                {t('no_active_trades')}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

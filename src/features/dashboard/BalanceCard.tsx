'use client';

import { useTranslations } from 'next-intl';

export default function BalanceCard() {
  const t = useTranslations('Dashboard');

  return (
    <div className="rounded-lg bg-white p-6 shadow-md">
      <h2 className="mb-4 text-xl font-semibold">{t('balance')}</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600">{t('total_balance')}</p>
          <p className="text-2xl font-bold">$0.00</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">{t('available_balance')}</p>
          <p className="text-2xl font-bold">$0.00</p>
        </div>
      </div>
    </div>
  );
}

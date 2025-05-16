'use client';

import { useTranslations } from 'next-intl';

export default function PnlChart() {
  const t = useTranslations('Dashboard');

  return (
    <div className="rounded-lg bg-white p-6 shadow-md">
      <h2 className="mb-4 text-xl font-semibold">{t('pnl_chart')}</h2>
      <div className="h-64 w-full">
        <div className="flex h-full items-center justify-center text-gray-500">
          {t('no_data_available')}
        </div>
      </div>
    </div>
  );
}

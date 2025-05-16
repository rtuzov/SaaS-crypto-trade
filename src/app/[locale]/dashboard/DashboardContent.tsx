'use client';

import { useTranslations } from 'next-intl';

import { withAuth } from '@/libs/withAuth';

function DashboardContent() {
  const t = useTranslations('Dashboard');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold">{t('meta_title')}</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Balance Card */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">{t('balance')}</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">{t('total_balance')}</span>
              <span className="font-semibold">$0.00</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">{t('available_balance')}</span>
              <span className="font-semibold">$0.00</span>
            </div>
          </div>
        </div>

        {/* Active Trades */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">{t('active_trades')}</h2>
          <div className="text-center text-gray-600">
            {t('no_active_trades')}
          </div>
        </div>

        {/* PnL Chart */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">{t('pnl_chart')}</h2>
          <div className="text-center text-gray-600">
            {t('no_data_available')}
          </div>
        </div>
      </div>
    </div>
  );
}

export default withAuth(['user', 'admin'])(DashboardContent);

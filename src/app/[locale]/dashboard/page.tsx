'use client';

import { useParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';

import { ActiveTradesTable } from '@/components/ActiveTradesTable';
import { BalanceCard } from '@/components/BalanceCard';
import { PnlChart } from '@/components/PnlChart';

export default function DashboardPage() {
  const params = useParams();
  const locale = params.locale as string;
  const { data: session } = useSession();
  const t = useTranslations('Dashboard');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold">{t('title')}</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Balance Card */}
        <BalanceCard />

        {/* PnL Chart */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">{t('pnl_chart')}</h2>
          {session?.user?.id && <PnlChart traderId={session.user.id} />}
        </div>

        {/* Active Trades */}
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">{t('active_trades')}</h2>
          {session?.user?.id && <ActiveTradesTable traderId={session.user.id} />}
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
        <div className="rounded-lg bg-blue-50 p-6">
          <h3 className="mb-4 text-xl font-semibold text-blue-800">{t('quick_actions')}</h3>
          <div className="space-y-4">
            <a
              href={`/${locale}/trade`}
              className="block rounded bg-blue-500 px-6 py-3 font-bold text-white hover:bg-blue-700"
            >
              {t('start_trading')}
            </a>
            <a
              href={`/${locale}/settings`}
              className="block rounded border border-blue-500 px-6 py-3 font-bold text-blue-500 hover:bg-blue-50"
            >
              {t('view_settings')}
            </a>
          </div>
        </div>

        <div className="rounded-lg bg-green-50 p-6">
          <h3 className="mb-4 text-xl font-semibold text-green-800">{t('account_summary')}</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                {t('email')}
              </label>
              <p className="mt-1 text-lg">{session?.user?.email}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                {t('language')}
              </label>
              <p className="mt-1 text-lg">{locale}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

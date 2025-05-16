'use client';

import { useParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';

export default function TradePage() {
  const params = useParams();
  const locale = params.locale as string;
  const { data: session } = useSession();
  const t = useTranslations('Trade');

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
        <h1 className="mb-8 text-4xl font-bold">{t('title')}</h1>

        <div className="w-full max-w-4xl rounded-lg bg-white p-8 shadow-lg">
          <div className="mb-6">
            <h2 className="mb-4 text-2xl font-semibold">{t('trading_platform')}</h2>
            <p className="text-lg text-gray-600">
              {t('welcome_message', { name: session?.user?.name || 'User' })}
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="rounded-lg bg-blue-50 p-6">
              <h3 className="mb-4 text-xl font-semibold text-blue-800">{t('market_overview')}</h3>
              <div className="space-y-4">
                <div className="rounded bg-white p-4 shadow">
                  <h4 className="mb-2 font-semibold">{t('btc_price')}</h4>
                  <p className="text-2xl font-bold text-green-600">$45,000</p>
                </div>
                <div className="rounded bg-white p-4 shadow">
                  <h4 className="mb-2 font-semibold">{t('eth_price')}</h4>
                  <p className="text-2xl font-bold text-green-600">$3,200</p>
                </div>
              </div>
            </div>

            <div className="rounded-lg bg-green-50 p-6">
              <h3 className="mb-4 text-xl font-semibold text-green-800">{t('trading_pairs')}</h3>
              <div className="space-y-4">
                <div className="rounded bg-white p-4 shadow">
                  <h4 className="mb-2 font-semibold">BTC/USDT</h4>
                  <p className="text-sm text-gray-600">
                    {t('volume')}
                    : $1.2B
                  </p>
                </div>
                <div className="rounded bg-white p-4 shadow">
                  <h4 className="mb-2 font-semibold">ETH/USDT</h4>
                  <p className="text-sm text-gray-600">
                    {t('volume')}
                    : $800M
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <a
              href={`/${locale}/dashboard`}
              className="rounded border border-blue-500 px-6 py-3 font-bold text-blue-500 hover:bg-blue-50"
            >
              {t('back_to_dashboard')}
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}

'use client';

import { useParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';

export default function SettingsPage() {
  const params = useParams();
  const locale = params.locale as string;
  const { data: session } = useSession();
  const t = useTranslations('Settings');

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
        <h1 className="mb-8 text-4xl font-bold">{t('title')}</h1>

        <div className="w-full max-w-2xl rounded-lg bg-white p-8 shadow-lg">
          <div className="mb-6">
            <h2 className="mb-4 text-2xl font-semibold">{t('profile')}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  {t('email')}
                </label>
                <p className="mt-1 text-lg">{session?.user?.email}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  {t('name')}
                </label>
                <p className="mt-1 text-lg">{session?.user?.name}</p>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="mb-4 text-2xl font-semibold">{t('preferences')}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  {t('language')}
                </label>
                <p className="mt-1 text-lg">{locale}</p>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <a
              href={`/${locale}/auth/logout`}
              className="rounded bg-red-500 px-6 py-3 font-bold text-white hover:bg-red-700"
            >
              {t('logout')}
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}

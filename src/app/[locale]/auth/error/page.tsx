'use client';

import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { useTranslations } from 'next-intl';

export default function AuthErrorPage() {
  const searchParams = useSearchParams();
  const error = searchParams.get('error');
  const errorDescription = searchParams.get('error_description');
  const t = useTranslations('Auth');

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
        <h1 className="mb-8 text-4xl font-bold text-red-600">{t('error_title')}</h1>

        <div className="mb-8 rounded-lg bg-red-50 p-6 text-left">
          <h2 className="mb-4 text-xl font-semibold text-red-800">{t('error_details')}</h2>
          <div className="space-y-2">
            <p className="text-red-700">
              <span className="font-semibold">
                {t('error_code')}
                :
              </span>
              {' '}
              {error || 'Unknown'}
            </p>
            {errorDescription && (
              <p className="text-red-700">
                <span className="font-semibold">
                  {t('error_description')}
                  :
                </span>
                {' '}
                {errorDescription}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-4">
          <Link
            href="/auth/login"
            className="block rounded bg-blue-500 px-6 py-3 font-bold text-white hover:bg-blue-700"
          >
            {t('try_again')}
          </Link>
          <Link
            href="/"
            className="block rounded border border-gray-300 px-6 py-3 font-bold text-gray-700 hover:bg-gray-50"
          >
            {t('back_to_home')}
          </Link>
        </div>
      </main>
    </div>
  );
}

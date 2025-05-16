import Link from 'next/link';
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'Index' });

  return {
    title: t('title'),
    description: t('description'),
  };
}

export default async function HomePage({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'Index' });

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
        <h1 className="mb-8 text-4xl font-bold">{t('title')}</h1>
        <p className="mb-8 text-xl text-gray-600">{t('description')}</p>

        <div className="mb-12 flex space-x-4">
          <Link
            href={`/${locale}/auth/login`}
            className="rounded bg-blue-500 px-6 py-3 font-bold text-white hover:bg-blue-700"
          >
            {t('get_started')}
          </Link>
          <Link
            href={`/${locale}/dashboard`}
            className="rounded border border-blue-500 px-6 py-3 font-bold text-blue-500 hover:bg-blue-50"
          >
            {t('learn_more')}
          </Link>
        </div>

        <div className="w-full max-w-4xl">
          <h2 className="mb-8 text-3xl font-bold">{t('features.title')}</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-4 text-xl font-semibold">{t('features.trading')}</h3>
              <p className="text-gray-600">{t('features.trading_desc')}</p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-4 text-xl font-semibold">{t('features.security')}</h3>
              <p className="text-gray-600">{t('features.security_desc')}</p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-4 text-xl font-semibold">{t('features.analytics')}</h3>
              <p className="text-gray-600">{t('features.analytics_desc')}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

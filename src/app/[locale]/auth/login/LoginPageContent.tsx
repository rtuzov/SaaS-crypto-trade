'use client';

import { useParams, useSearchParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';
import { useEffect } from 'react';

import { LoginButton } from './LoginButton';

export function LoginPageContent() {
  const { data: session, status } = useSession();
  const searchParams = useSearchParams();
  const params = useParams();
  const locale = params.locale as string;
  const callbackUrl = searchParams.get('callbackUrl') || `/${locale}`;
  const t = useTranslations('Auth');

  useEffect(() => {
    if (status === 'authenticated' && session) {
      window.location.href = callbackUrl;
    }
  }, [status, session, callbackUrl]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
        <h1 className="mb-8 text-4xl font-bold">{t('sign_in')}</h1>
        <div className="w-full max-w-xs">
          <LoginButton />
        </div>
      </main>
    </div>
  );
}

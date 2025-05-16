'use client';

import { useParams, useSearchParams } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { useTranslations } from 'next-intl';

export function LoginButton() {
  const searchParams = useSearchParams();
  const params = useParams();
  const locale = params.locale as string;
  const callbackUrl = searchParams.get('callbackUrl') || `/${locale}`;
  const t = useTranslations('Auth');

  const handleSignIn = () => {
    signIn('keycloak', { callbackUrl });
  };

  return (
    <button
      onClick={handleSignIn}
      className="w-full rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
    >
      {t('sign_in_with_keycloak')}
    </button>
  );
}

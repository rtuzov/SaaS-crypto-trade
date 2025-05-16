// src/app/[locale]/auth/login/page.tsx
import { getTranslations } from 'next-intl/server';

import { LoginPageContent } from './LoginPageContent';

export async function generateMetadata({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'Auth' });

  return {
    title: t('sign_in'),
    description: t('sign_in_with_keycloak'),
  };
}

export default function LoginPage() {
  return <LoginPageContent />;
}

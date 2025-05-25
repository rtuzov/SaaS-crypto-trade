'use client';

import { SessionProvider } from 'next-auth/react';
import { NextIntlClientProvider } from 'next-intl';

import { ClientProviders } from '@/components/ClientProviders';

export function Providers({ children, locale, messages }: { children: React.ReactNode; locale: string; messages: any }) {
  return (
    <SessionProvider>
      <NextIntlClientProvider locale={locale} messages={messages} timeZone="UTC">
        <ClientProviders>
          {children}
        </ClientProviders>
      </NextIntlClientProvider>
    </SessionProvider>
  );
}

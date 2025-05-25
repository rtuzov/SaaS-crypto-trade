"use client";
import { Provider } from "urql";
import { urqlClient } from "@/libs/graphqlClient";
import { NextIntlClientProvider } from 'next-intl';
import { SessionProvider } from 'next-auth/react';
import { ThemeProvider } from 'next-themes';
import { ReactNode } from 'react';

export function Providers({ children, locale, messages }: { children: ReactNode, locale: string, messages: any }) {
  return (
    <SessionProvider>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <NextIntlClientProvider locale={locale} messages={messages} timeZone="UTC">
          <Provider value={urqlClient}>{children}</Provider>
        </NextIntlClientProvider>
      </ThemeProvider>
    </SessionProvider>
  );
} 
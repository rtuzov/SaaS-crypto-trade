'use client';

import { SessionProvider } from 'next-auth/react';

import { ClientProviders } from '@/components/ClientProviders';
import { ThemeProvider } from '@/components/ui/theme-provider';
import { Toaster } from '@/components/ui/toaster';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        <ClientProviders>
          {children}
          <Toaster />
        </ClientProviders>
      </ThemeProvider>
    </SessionProvider>
  );
}

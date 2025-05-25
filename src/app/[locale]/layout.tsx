import '@/styles/global.css';
import { getTranslations } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Providers } from '@/app/providers';
import { ReactNode } from 'react';
import en from '@/messages/en.json';
import ru from '@/messages/ru.json';
import zh from '@/messages/zh.json';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

const messagesMap: Record<string, any> = { en, ru, zh };

export async function generateMetadata({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'Metadata' });
  
  return {
    title: t('title'),
    description: t('description'),
  };
}

export function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'ru' }, { locale: 'zh' }];
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: ReactNode;
  params: { locale: string };
}) {
  // Validate that the incoming locale is valid
  const locales = ['en', 'ru', 'zh'];
  
  if (!locales.includes(locale)) {
    notFound();
  }
  
  const messages = await getMessages({ locale });
  
  return (
    <html lang={locale}>
      <body className="min-h-screen flex flex-col">
        <Providers locale={locale} messages={messages}>
          <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}

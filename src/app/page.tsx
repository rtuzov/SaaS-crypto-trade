import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

import { AppConfig } from '@/utils/AppConfig';

export default function RootPage() {
  const headersList = headers();
  const acceptLanguage = headersList.get('accept-language') || '';

  // Try to detect user's preferred language
  const preferredLocale = acceptLanguage
    .split(',')
    .map(lang => lang.split(';')[0]?.trim() || '')
    .find(lang => AppConfig.locales.includes(lang as any)) || AppConfig.defaultLocale;

  redirect(`/${preferredLocale}`);
}

import { notFound } from 'next/navigation';
import { getRequestConfig } from 'next-intl/server';

import { type Locale, locales } from '@/utils/AppConfig';

export { locales };
export type { Locale };

export default getRequestConfig(async ({ locale }) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as Locale)) {
    notFound();
  }

  return {
    messages: (await import(`@/messages/${locale}.json`)).default,
    locale: locale as Locale,
    timeZone: 'UTC',
  };
});

import { getRequestConfig } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { localeConfig } from '../utils/AppConfig';
import en from '../messages/en.json';
import ru from '../messages/ru.json';
import zh from '../messages/zh.json';

const messagesMap: Record<string, any> = { en, ru, zh };

export default getRequestConfig(async ({ locale }) => {
  if (!locale || !localeConfig.locales.includes(locale as (typeof localeConfig.locales)[number])) {
    notFound();
  }

  const messages = messagesMap[locale as keyof typeof messagesMap];
  if (!messages) {
    notFound();
  }

  return {
    locale,
    messages,
    timeZone: 'Europe/Moscow',
    now: new Date(),
    formats: {
      dateTime: {
        short: {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
        },
        medium: {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        },
        long: {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
          hour: 'numeric',
          minute: 'numeric',
        },
      },
    },
  };
}); 
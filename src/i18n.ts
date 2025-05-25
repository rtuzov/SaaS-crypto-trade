import { getRequestConfig } from 'next-intl/server';
import { localeConfig } from './utils/AppConfig';
import en from './messages/en.json';
import ru from './messages/ru.json';
import zh from './messages/zh.json';

export const locales = localeConfig.locales;
export const defaultLocale = localeConfig.defaultLocale;
export const localePrefix = localeConfig.localePrefix;

const messagesMap: Record<string, any> = { en, ru, zh };

export default getRequestConfig(async ({ locale }) => {
  return {
    messages: messagesMap[locale as keyof typeof messagesMap],
    timeZone: 'UTC'
  };
}); 
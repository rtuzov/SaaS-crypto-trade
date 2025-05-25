import { defineRouting } from 'next-intl/routing';
import { localeConfig } from './src/utils/AppConfig';

export default defineRouting({
  locales: localeConfig.locales,
  defaultLocale: localeConfig.defaultLocale,
  localePrefix: localeConfig.localePrefix,
}); 
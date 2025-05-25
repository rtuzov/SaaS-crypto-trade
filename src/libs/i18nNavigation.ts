import { createNavigation } from 'next-intl/navigation';
import { localeConfig } from '@/utils/AppConfig';

export const { Link, redirect, usePathname, useRouter } = createNavigation({
  locales: localeConfig.locales,
  defaultLocale: localeConfig.defaultLocale,
});

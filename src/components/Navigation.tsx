'use client';

import { Link, usePathname } from '@/libs/i18nNavigation';
import { useLocale } from 'next-intl';
import { cn } from '@/libs/utils';

type NavItem = {
  href: string;
  label: string;
};

const NAV_ITEMS: NavItem[] = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/trade', label: 'Trade' },
  { href: '/analytics', label: 'Analytics' },
  { href: '/pricing', label: 'Pricing' },
  { href: '/settings', label: 'Settings' },
];

export function Navigation() {
  const pathname = usePathname();
  const locale = useLocale();

  return (
    <nav>
      <ul className="flex gap-6">
        {NAV_ITEMS.map(({ href, label }) => {
          const active = pathname === `/${locale}${href}`;
          return (
            <li key={href}>
              <Link
                href={href}
                className={cn(
                  'text-sm font-medium transition-colors hover:text-primary',
                  active ? 'text-primary' : 'text-muted-foreground'
                )}
              >
                {label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

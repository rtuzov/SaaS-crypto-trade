'use client';

import { useSession, signIn, signOut } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Icons } from '@/components/ui/icons';
import { useTranslations } from 'next-intl';
import { Link, usePathname } from '@/libs/i18nNavigation';

export function Navbar() {
  const { data: session, status } = useSession();
  const pathname = usePathname();
  const t = useTranslations('Navigation');
  const appName = useTranslations('app');
  const authT = useTranslations('Auth');
  
  const isActive = (path: string) => {
    return pathname.startsWith(path);
  };
  
  return (
    <header className="border-b bg-background">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center space-x-2">
            <Icons.logo className="h-6 w-6" />
            <span className="font-bold">{appName('name')}</span>
          </Link>
          
          <nav className="hidden md:flex gap-6">
            <Link
              href="/dashboard"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isActive('/dashboard') ? 'text-primary' : 'text-muted-foreground'
              }`}
            >
              {t('dashboard')}
            </Link>
            <Link
              href="/trade"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isActive('/trade') ? 'text-primary' : 'text-muted-foreground'
              }`}
            >
              {t('trade')}
            </Link>
            <Link
              href="/analytics"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isActive('/analytics') ? 'text-primary' : 'text-muted-foreground'
              }`}
            >
              {t('analytics')}
            </Link>
          </nav>
        </div>
        
        <div className="flex items-center gap-4">
          {status === 'loading' ? (
            <Icons.spinner className="h-4 w-4 animate-spin" />
          ) : session ? (
            <div className="flex items-center gap-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">
                  {t('account')}
                </Button>
              </Link>
              <Button variant="outline" size="sm" onClick={() => signOut()}>
                {authT('logout')}
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" onClick={() => signIn('keycloak')}>
                {authT('login')}
              </Button>
              <Link href="/auth/register">
                <Button size="sm">{authT('register')}</Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
} 
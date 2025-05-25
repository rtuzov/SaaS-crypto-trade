'use client';

import { Icons } from '@/components/ui/icons';
import { useTranslations } from 'next-intl';
import { Link } from '@/libs/i18nNavigation';

export function Footer() {
  const t = useTranslations('Footer');
  const appName = useTranslations('app');
  
  return (
    <footer className="border-t bg-background">
      <div className="container py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Icons.logo className="h-6 w-6" />
              <span className="font-bold">{appName('name')}</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {t('description')}
            </p>
          </div>
          
          <div>
            <h3 className="font-medium mb-3">{t('platform')}</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/dashboard" className="text-muted-foreground hover:text-foreground">
                  {t('dashboard')}
                </Link>
              </li>
              <li>
                <Link href="/trade" className="text-muted-foreground hover:text-foreground">
                  {t('trade')}
                </Link>
              </li>
              <li>
                <Link href="/analytics" className="text-muted-foreground hover:text-foreground">
                  {t('analytics')}
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium mb-3">{t('company')}</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/about" className="text-muted-foreground hover:text-foreground">
                  {t('about')}
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="text-muted-foreground hover:text-foreground">
                  {t('pricing')}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-foreground">
                  {t('contact')}
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium mb-3">{t('legal')}</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/terms" className="text-muted-foreground hover:text-foreground">
                  {t('terms')}
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-muted-foreground hover:text-foreground">
                  {t('privacy')}
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8 border-t pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} {appName('name')}. {t('copyright')}
          </p>
          
          <div className="flex space-x-4 mt-4 md:mt-0">
            <a href="https://twitter.com" className="text-muted-foreground hover:text-foreground" target="_blank" rel="noopener noreferrer">
              <Icons.twitter className="h-5 w-5" />
              <span className="sr-only">Twitter</span>
            </a>
            <a href="https://github.com" className="text-muted-foreground hover:text-foreground" target="_blank" rel="noopener noreferrer">
              <Icons.gitHub className="h-5 w-5" />
              <span className="sr-only">GitHub</span>
            </a>
            <a href="https://t.me" className="text-muted-foreground hover:text-foreground" target="_blank" rel="noopener noreferrer">
              <Icons.telegram className="h-5 w-5" />
              <span className="sr-only">Telegram</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
} 
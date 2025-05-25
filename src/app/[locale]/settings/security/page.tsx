"use client";

import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export default function Security() {
  const t = useTranslations('settings.security');

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">{t('title')}</h2>
      <Button>{t('enable2fa')}</Button>
    </div>
  );
} 
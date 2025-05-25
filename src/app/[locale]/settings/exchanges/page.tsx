"use client";

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export default function Exchanges() {
  const t = useTranslations('settings.exchanges');

  return (
    <div className="grid gap-4 max-w-md">
      <label className="grid gap-1">
        <span>API Key</span>
        <Input />
      </label>
      <label className="grid gap-1">
        <span>API Secret</span>
        <Input type="password" />
      </label>
      <Button>{t('testButton')}</Button>
    </div>
  );
} 
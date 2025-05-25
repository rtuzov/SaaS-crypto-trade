"use client";

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export default function Profile() {
  const t = useTranslations('settings.profile');

  return (
    <div className="grid gap-4 max-w-md">
      <label className="grid gap-1">
        <span>{t('name')}</span>
        <Input />
      </label>
      <Button>{t('save')}</Button>
    </div>
  );
} 
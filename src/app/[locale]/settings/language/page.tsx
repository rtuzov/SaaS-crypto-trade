"use client";

import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Button } from '@/components/ui/button';
import { useRouter, usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';

export default function Language({ params }: any) {
  const t = useTranslations('settings.language');
  const router = useRouter();
  const path = usePathname().split('/').slice(2).join('/');

  const save = async (loc: string) => router.replace(`/${loc}/${path}`);

  return (
    <div className="space-y-4">
      <RadioGroup defaultValue={params.locale} onValueChange={save}>
        {['en', 'ru', 'zh'].map((l) => (
          <div key={l} className="flex items-center gap-2">
            <RadioGroupItem value={l} id={l} /> <label htmlFor={l}>{l.toUpperCase()}</label>
          </div>
        ))}
      </RadioGroup>
      <Button>{t('save')}</Button>
    </div>
  );
} 
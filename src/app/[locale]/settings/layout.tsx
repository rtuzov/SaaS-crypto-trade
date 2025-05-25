import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ReactNode } from 'react';
import { useTranslations } from 'next-intl';

export default function SettingsLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: { locale: string };
}) {
  const t = useTranslations('settings');
  const tabs = ['profile', 'security', 'exchanges', 'language'] as const;
  // Active tab detection based on segment passed from page component or default
  const active = (children as any)?.props?.segment ?? 'profile';

  return (
    <section className="container py-10">
      <h1 className="text-3xl font-bold mb-6">{t('title')}</h1>
      <Tabs defaultValue={active} className="w-full">
        <TabsList>
          {tabs.map((tab) => (
            <TabsTrigger key={tab} value={tab} asChild>
              {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
              <a href={`/${params.locale}/settings/${tab}`}>{t(`${tab}.title`)}</a>
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value={active} className="pt-8">
          {children}
        </TabsContent>
      </Tabs>
    </section>
  );
} 
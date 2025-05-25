import { getTranslations } from 'next-intl/server';

export default async function SettingsPage({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale });

  return (
    <div className="container py-10 space-y-6">
      <h1 className="text-3xl font-bold">
        {t('settings.title', { default: 'Settings' })}
      </h1>
      <p className="text-muted-foreground">
        {t('settings.subtitle', { default: 'Manage your account preferences.' })}
      </p>
      {/* TODO: Add settings forms */}
    </div>
  );
} 
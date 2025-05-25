import { Sidebar } from '@/components/common/Sidebar';
import { ReactNode } from 'react';
import { useTranslations } from 'next-intl';

export default function AdminLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: { locale: string };
}) {
  const t = useTranslations('admin.sidebar');

  const links = [
    { href: `/${params.locale}/admin/users`, label: t('users') },
    { href: `/${params.locale}/admin/plans`, label: t('plans') },
    { href: `/${params.locale}/admin/logs`, label: t('logs') },
    { href: `/${params.locale}/admin/services`, label: t('services') },
  ];

  return (
    <div className="flex">
      <Sidebar links={links} />
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
} 
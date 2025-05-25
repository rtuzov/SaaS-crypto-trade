'use client';

import { useSession } from 'next-auth/react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { useTranslations } from 'next-intl';

export function UserProfile() {
  const { data: session } = useSession();
  const t = useTranslations('Dashboard.profile');
  
  if (!session?.user) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{t('title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{t('login_to_view')}</p>
        </CardContent>
      </Card>
    );
  }
  
  // Получаем первые буквы имени для аватара
  const initials = session.user.name
    ? session.user.name
        .split(' ')
        .map((n) => n[0])
        .join('')
    : 'U';
    
  // Проверяем роли пользователя
  const roles = session.user.roles || [];
  const isAdmin = roles.includes('admin');
  const isTrader = roles.includes('trader');
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center space-x-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src={session.user.image || ''} alt={session.user.name || t('user')} />
            <AvatarFallback>{initials}</AvatarFallback>
          </Avatar>
          
          <div>
            <h3 className="text-lg font-medium">{session.user.name || t('user')}</h3>
            <p className="text-sm text-muted-foreground">{session.user.email}</p>
            
            <div className="mt-2 flex flex-wrap gap-2">
              {isAdmin && <Badge>{t('admin')}</Badge>}
              {isTrader && <Badge>{t('trader')}</Badge>}
              {roles.filter(role => role !== 'admin' && role !== 'trader').map((role) => (
                <Badge key={role} variant="outline">{role}</Badge>
              ))}
            </div>
          </div>
        </div>
        
        <div className="pt-4 border-t">
          <h4 className="text-sm font-medium mb-2">{t('account_info')}</h4>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="text-sm text-muted-foreground">{t('user_id')}</dt>
              <dd className="text-sm font-medium">{session.user.id || t('not_specified')}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm text-muted-foreground">{t('registration_date')}</dt>
              <dd className="text-sm font-medium">
                {/* Это заглушка, в реальном приложении нужно получать из API */}
                {new Date().toLocaleDateString()}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm text-muted-foreground">{t('status')}</dt>
              <dd className="text-sm font-medium">
                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                  {t('active')}
                </Badge>
              </dd>
            </div>
          </dl>
        </div>
      </CardContent>
    </Card>
  );
} 
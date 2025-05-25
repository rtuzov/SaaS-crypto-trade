import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
// Заглушка для Select
const Select = (props: any) => <select {...props} />;
const SelectContent = (props: any) => <div {...props} />;
const SelectItem = (props: any) => <option {...props} />;
const SelectTrigger = (props: any) => <div {...props} />;
const SelectValue = (props: any) => <div {...props} />;
import { useTranslations } from 'next-intl'

export function EquityCurve() {
  const t = useTranslations('analytics')
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">
          {t('equity.title')}
        </CardTitle>
        <Select defaultValue="1y">
          <SelectTrigger className="w-[100px]">
            <SelectValue placeholder={t('equity.period')} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1m">{t('equity.periods.1m')}</SelectItem>
            <SelectItem value="3m">{t('equity.periods.3m')}</SelectItem>
            <SelectItem value="6m">{t('equity.periods.6m')}</SelectItem>
            <SelectItem value="1y">{t('equity.periods.1y')}</SelectItem>
            <SelectItem value="all">{t('equity.periods.all')}</SelectItem>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] flex items-center justify-center text-muted-foreground">
          TradingView Chart Placeholder
        </div>
      </CardContent>
    </Card>
  )
} 
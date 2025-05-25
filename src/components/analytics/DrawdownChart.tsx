import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useTranslations } from 'next-intl'

export function DrawdownChart() {
  const t = useTranslations('analytics')
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          {t('drawdown.title')}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] flex items-center justify-center text-muted-foreground">
          TradingView Chart Placeholder
        </div>
      </CardContent>
    </Card>
  )
} 
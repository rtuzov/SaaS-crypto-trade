import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useTranslations } from 'next-intl'
import { TrendingUp, TrendingDown, BarChart, DollarSign } from 'lucide-react'

const metrics = [
  {
    title: 'totalReturn',
    value: '+156.7%',
    icon: TrendingUp,
    color: 'text-green-500'
  },
  {
    title: 'maxDrawdown',
    value: '-12.3%',
    icon: TrendingDown,
    color: 'text-red-500'
  },
  {
    title: 'sharpeRatio',
    value: '2.1',
    icon: BarChart,
    color: 'text-blue-500'
  },
  {
    title: 'profitFactor',
    value: '3.2',
    icon: DollarSign,
    color: 'text-purple-500'
  }
]

export function MetricsGrid() {
  const t = useTranslations('analytics')
  
  return (
    <div className="grid grid-cols-2 gap-4">
      {metrics.map((metric) => (
        <Card key={metric.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {t(`metrics.${metric.title}`)}
            </CardTitle>
            <metric.icon className={`h-4 w-4 ${metric.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metric.value}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
} 
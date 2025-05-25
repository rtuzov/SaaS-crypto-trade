import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, TrendingDown, BarChart } from 'lucide-react'

const stats = [
  {
    title: 'Win Rate',
    value: '68%',
    icon: TrendingUp,
    color: 'text-green-500'
  },
  {
    title: 'Avg R/R',
    value: '1.5',
    icon: BarChart,
    color: 'text-blue-500'
  },
  {
    title: 'Max Drawdown',
    value: '-12.3%',
    icon: TrendingDown,
    color: 'text-red-500'
  }
]

export function QuickStats() {
  return (
    <>
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {stat.title}
            </CardTitle>
            <stat.icon className={`h-4 w-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
          </CardContent>
        </Card>
      ))}
    </>
  )
} 
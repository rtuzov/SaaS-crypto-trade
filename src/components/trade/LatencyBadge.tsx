import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Clock } from 'lucide-react'

export function LatencyBadge() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">
          Задержка
        </CardTitle>
        <Clock className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <Badge variant="default" className="text-lg">
            245ms
          </Badge>
          <span className="text-sm text-muted-foreground">
            Последнее обновление: 10:30:15
          </span>
        </div>
      </CardContent>
    </Card>
  )
} 
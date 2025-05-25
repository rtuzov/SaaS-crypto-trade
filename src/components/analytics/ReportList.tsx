import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
// Заглушка для ScrollArea
const ScrollArea = (props: any) => <div {...props} />;
import { useTranslations } from 'next-intl'
import { Download, FileText } from 'lucide-react'

const reports = [
  {
    id: 1,
    name: 'report1',
    date: '2024-03-15',
    size: '2.4 MB'
  },
  {
    id: 2,
    name: 'report2',
    date: '2024-03-14',
    size: '1.8 MB'
  },
  {
    id: 3,
    name: 'report3',
    date: '2024-03-13',
    size: '3.2 MB'
  }
]

export function ReportList() {
  const t = useTranslations('analytics')
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          {t('reports.title')}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px]">
          <div className="space-y-4">
            {reports.map((report) => (
              <div
                key={report.id}
                className="flex items-center justify-between p-4 bg-muted rounded-lg"
              >
                <div className="flex items-center space-x-4">
                  <FileText className="h-8 w-8 text-muted-foreground" />
                  <div>
                    <h4 className="font-medium">
                      {t(`reports.${report.name}`)}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {report.date} · {report.size}
                    </p>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  {t('reports.download')}
                </Button>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
} 
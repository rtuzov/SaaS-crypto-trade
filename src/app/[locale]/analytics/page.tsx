import { UploadZone } from '@/components/analytics/UploadZone'
import { MetricsGrid } from '@/components/analytics/MetricsGrid'
import { EquityCurve } from '@/components/analytics/EquityCurve'
import { DrawdownChart } from '@/components/analytics/DrawdownChart'
import { ReportList } from '@/components/analytics/ReportList'

export default function AnalyticsPage() {
  return (
    <main className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <UploadZone />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <MetricsGrid />
          <EquityCurve />
        </div>
        
        <DrawdownChart />
        <ReportList />
      </div>
    </main>
  )
} 
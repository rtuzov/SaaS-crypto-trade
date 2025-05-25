import { SignalChat } from '@/components/trade/SignalChat'
import { QuickForm } from '@/components/trade/QuickForm'
import { LatencyBadge } from '@/components/trade/LatencyBadge'
import { TradeHistory } from '@/components/trade/TradeHistory'

export default function TradePage() {
  return (
    <main className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <SignalChat />
          <QuickForm />
        </div>
        <div>
          <div className="sticky top-6 space-y-6">
            <LatencyBadge />
            <TradeHistory />
          </div>
        </div>
      </div>
    </main>
  )
} 
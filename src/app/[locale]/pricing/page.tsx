import { PricingTable } from '@/components/pricing/PricingTable'
import { AddOns } from '@/components/pricing/AddOns'
import { PricingFAQ } from '@/components/pricing/PricingFAQ'

export default function PricingPage() {
  return (
    <main className="min-h-screen py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-12">
          Тарифы и цены
        </h1>
        
        <PricingTable />
        <AddOns />
        <PricingFAQ />
      </div>
    </main>
  )
} 
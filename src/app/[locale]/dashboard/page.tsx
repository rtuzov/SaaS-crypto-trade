'use client';

import BalanceCard from '@/features/dashboard/BalanceCard'
import { TitleBar } from '@/features/dashboard/TitleBar'
import { Button } from '@/components/ui/button'
import { History } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useEffect, useRef } from 'react'
import { useTheme } from 'next-themes'
import { applyChartTheme } from '@/libs/applyChartTheme'
import { ThemeToggle } from '@/components/common/ThemeToggle'
import { Link } from '@/libs/i18nNavigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function DashboardPage() {
  const t = useTranslations('Dashboard')
  const chartRef = useRef<any>(null)
  const { theme } = useTheme()
  

  // Эмуляция создания графика
  useEffect(() => {
    // В реальном приложении здесь будет создание графика TradingView
    const chart = chartRef.current
    if (chart) {
      applyChartTheme(chart, theme === 'dark')
    }
  }, [theme])
  
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <ThemeToggle />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <TitleBar title={t('profile.title')} description={t('profile.account_info')} />
        <BalanceCard />
      </div>
      
      <div className="mt-8">
        <Link href="/dashboard/transactions">
          <Button variant="outline" className="flex items-center gap-2">
            <History className="h-4 w-4" />
            {t('transactions')}
          </Button>
        </Link>
      </div>
    </main>
  )
} 
'use client';

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Check, X } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: {
      monthly: 'Бесплатно',
      yearly: 'Бесплатно'
    },
    features: {
      'Автоторговля': false,
      'Telegram-сигналы': true,
      'Базовые стратегии': true,
      'Историческая аналитика': true,
      'API доступ': false,
      'Приоритетная поддержка': false,
      'Персональный менеджер': false
    }
  },
  {
    name: 'Pro',
    price: {
      monthly: '$29/мес',
      yearly: '$290/год'
    },
    features: {
      'Автоторговля': true,
      'Telegram-сигналы': true,
      'Базовые стратегии': true,
      'Историческая аналитика': true,
      'API доступ': true,
      'Приоритетная поддержка': true,
      'Персональный менеджер': false
    },
    highlighted: true
  },
  {
    name: 'Enterprise',
    price: {
      monthly: 'По запросу',
      yearly: 'По запросу'
    },
    features: {
      'Автоторговля': true,
      'Telegram-сигналы': true,
      'Базовые стратегии': true,
      'Историческая аналитика': true,
      'API доступ': true,
      'Приоритетная поддержка': true,
      'Персональный менеджер': true
    }
  }
]

export function PricingTable() {
  const [isYearly, setIsYearly] = useState(false)
  
  return (
    <div className="mb-20">
      <div className="flex items-center justify-center gap-4 mb-8">
        <span className={!isYearly ? 'font-semibold' : ''}>Ежемесячно</span>
        <Switch
          checked={isYearly}
          onCheckedChange={setIsYearly}
        />
        <span className={isYearly ? 'font-semibold' : ''}>
          Ежегодно <span className="text-primary">-10%</span>
        </span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`bg-white rounded-lg shadow-lg p-8 ${
              plan.highlighted ? 'ring-2 ring-primary' : ''
            }`}
          >
            <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
            <p className="text-3xl font-bold mb-6">
              {isYearly ? plan.price.yearly : plan.price.monthly}
            </p>
            
            <ul className="space-y-4 mb-8">
              {Object.entries(plan.features).map(([feature, included]) => (
                <li key={feature} className="flex items-center">
                  {included ? (
                    <Check className="w-5 h-5 text-primary mr-2" />
                  ) : (
                    <X className="w-5 h-5 text-gray-400 mr-2" />
                  )}
                  {feature}
                </li>
              ))}
            </ul>
            
            <Button
              className="w-full"
              variant={plan.highlighted ? 'default' : 'outline'}
            >
              Выбрать план
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
} 
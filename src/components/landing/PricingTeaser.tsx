import { Button } from '@/components/ui/button'
import { Check } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: 'Бесплатно',
    features: [
      'Базовые стратегии',
      'Telegram-уведомления',
      'Историческая аналитика',
      'Поддержка в чате'
    ]
  },
  {
    name: 'Pro',
    price: '$29/мес',
    features: [
      'Все функции Starter',
      'Продвинутые стратегии',
      'API доступ',
      'Приоритетная поддержка',
      'Персональный менеджер'
    ],
    highlighted: true
  }
]

export function PricingTeaser() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          Выберите свой тариф
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`bg-white rounded-lg shadow-lg p-8 ${
                plan.highlighted ? 'ring-2 ring-primary' : ''
              }`}
            >
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <p className="text-3xl font-bold mb-6">{plan.price}</p>
              
              <ul className="space-y-4 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center">
                    <Check className="w-5 h-5 text-primary mr-2" />
                    {feature}
                  </li>
                ))}
              </ul>
              
              <Button
                className="w-full"
                variant={plan.highlighted ? 'default' : 'outline'}
              >
                Начать сейчас
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
} 
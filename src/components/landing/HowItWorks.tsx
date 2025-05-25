import { motion } from 'framer-motion'
import { Key, Send, TrendingUp } from 'lucide-react'

const steps = [
  {
    icon: Key,
    title: 'Подключи ключ',
    description: 'Добавьте API ключ от вашей биржи'
  },
  {
    icon: Send,
    title: 'Отправь команду',
    description: 'Выберите стратегию и настройте параметры'
  },
  {
    icon: TrendingUp,
    title: 'Смотри PnL',
    description: 'Отслеживайте прибыль в реальном времени'
  }
]

export function HowItWorks() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold text-center mb-12"
        >
          Как это работает
        </motion.h2>
        
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              className="flex flex-col items-center text-center relative"
            >
              <div className="bg-primary/10 p-4 rounded-full mb-4">
                <step.icon className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
              
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gray-300" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
} 
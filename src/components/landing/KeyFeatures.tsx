import { motion } from 'framer-motion'
import { Bot, LineChart, Shield, MessageSquare } from 'lucide-react'

const features = [
  {
    icon: Bot,
    title: 'Автоторговля',
    description: 'Автоматическое исполнение сделок по заданным стратегиям'
  },
  {
    icon: LineChart,
    title: 'Ретро-аналитика',
    description: 'Глубокий анализ исторических данных для оптимизации стратегий'
  },
  {
    icon: MessageSquare,
    title: 'Telegram-сигналы',
    description: 'Мгновенные уведомления о торговых сигналах в Telegram'
  },
  {
    icon: Shield,
    title: 'Безопасность',
    description: 'Многоуровневая защита ваших средств и данных'
  }
]

export function KeyFeatures() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold text-center mb-12"
        >
          Ключевые особенности
        </motion.h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
            >
              <feature.icon className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
} 
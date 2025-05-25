import { motion } from 'framer-motion'

const testimonials = [
  {
    avatar: '/avatars/user1.jpg',
    name: 'Александр К.',
    quote: 'Сервис полностью изменил мой подход к торговле. Теперь я могу сосредоточиться на стратегии, а не на рутинных операциях.'
  },
  {
    avatar: '/avatars/user2.jpg',
    name: 'Мария П.',
    quote: 'Отличная платформа для автоматизации торговли. Особенно нравятся Telegram-уведомления и аналитика.'
  },
  {
    avatar: '/avatars/user3.jpg',
    name: 'Дмитрий В.',
    quote: 'Благодаря этому сервису я смог систематизировать свою торговлю и увеличить прибыль на 30%.'
  }
]

export function Testimonials() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold text-center mb-12"
        >
          Отзывы пользователей
        </motion.h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              className="bg-white p-6 rounded-lg shadow-lg"
            >
              <div className="flex items-center mb-4">
                <img
                  src={testimonial.avatar}
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full mr-4"
                />
                <h3 className="font-semibold">{testimonial.name}</h3>
              </div>
              <p className="text-gray-600 italic">"{testimonial.quote}"</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
} 
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'

const faqs = [
  {
    question: 'Как происходит оплата?',
    answer: 'Мы принимаем оплату картами Visa/Mastercard, а также криптовалютой (BTC, ETH, USDT).'
  },
  {
    question: 'Можно ли отменить подписку?',
    answer: 'Да, вы можете отменить подписку в любой момент. Средства за неиспользованный период будут возвращены.'
  },
  {
    question: 'Есть ли пробный период?',
    answer: 'Да, мы предоставляем 14-дневный пробный период для всех платных тарифов.'
  },
  {
    question: 'Как перейти на другой тариф?',
    answer: 'Вы можете изменить тариф в любой момент в настройках аккаунта. Изменения вступят в силу со следующего платежного периода.'
  }
]

export function PricingFAQ() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-center mb-8">
        Часто задаваемые вопросы
      </h2>
      
      <div className="max-w-3xl mx-auto">
        <Accordion type="single" collapsible className="w-full">
          {faqs.map((faq, index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger className="text-left">
                {faq.question}
              </AccordionTrigger>
              <AccordionContent>
                {faq.answer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </div>
  )
} 
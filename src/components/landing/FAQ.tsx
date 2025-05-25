import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'

const faqs = [
  {
    question: 'Как начать использовать сервис?',
    answer: 'Зарегистрируйтесь, подключите API ключ от биржи и выберите стратегию торговли.'
  },
  {
    question: 'Какие биржи поддерживаются?',
    answer: 'В настоящее время поддерживаются Binance, Bybit и OKX. Мы постоянно добавляем новые биржи.'
  },
  {
    question: 'Безопасно ли использовать API ключи?',
    answer: 'Да, мы используем шифрование и храним ключи в защищенном хранилище. Доступ к торговле можно ограничить по IP.'
  },
  {
    question: 'Как работает автоматическая торговля?',
    answer: 'Вы выбираете стратегию, настраиваете параметры, и система автоматически исполняет сделки по заданным правилам.'
  },
  {
    question: 'Можно ли тестировать стратегии на исторических данных?',
    answer: 'Да, у нас есть встроенный бэктестер для тестирования стратегий на исторических данных.'
  },
  {
    question: 'Как часто приходят сигналы в Telegram?',
    answer: 'Сигналы приходят в реальном времени, как только система обнаруживает торговую возможность.'
  },
  {
    question: 'Есть ли мобильное приложение?',
    answer: 'Да, мы предоставляем мобильное приложение для iOS и Android с основными функциями.'
  },
  {
    question: 'Какой минимальный депозит требуется?',
    answer: 'Минимальный депозит зависит от выбранной биржи и стратегии. Обычно это от $100.'
  }
]

export function FAQ() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          Часто задаваемые вопросы
        </h2>
        
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
    </section>
  )
} 
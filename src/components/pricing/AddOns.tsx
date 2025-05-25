import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'

const addOns = [
  {
    id: 'crypto-payments',
    name: 'Крипто-платежи',
    description: 'Возможность оплаты в BTC, ETH и других криптовалютах',
    price: 'Бесплатно'
  },
  {
    id: 'api-access',
    name: 'API-доступ',
    description: 'Полный доступ к API для интеграции с вашими системами',
    price: '+$10/мес'
  }
]

export function AddOns() {
  return (
    <div className="mb-20">
      <h2 className="text-2xl font-bold text-center mb-8">
        Дополнительные опции
      </h2>
      
      <div className="max-w-2xl mx-auto space-y-4">
        {addOns.map((addOn) => (
          <div
            key={addOn.id}
            className="flex items-start space-x-4 p-4 bg-white rounded-lg shadow"
          >
            <Checkbox id={addOn.id} />
            <div className="flex-1">
              <Label
                htmlFor={addOn.id}
                className="text-lg font-semibold flex items-center justify-between"
              >
                {addOn.name}
                <span className="text-primary">{addOn.price}</span>
              </Label>
              <p className="text-gray-600 mt-1">{addOn.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
} 
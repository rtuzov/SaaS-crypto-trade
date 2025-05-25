import { ForgotForm } from '@/components/auth/ForgotForm'

export default function ForgotPage() {
  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8">
          Восстановление пароля
        </h1>
        
        <ForgotForm />
      </div>
    </main>
  )
} 
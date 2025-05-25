'use client';

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Icons } from '@/components/ui/icons'

export function ForgotForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [isSent, setIsSent] = useState(false)
  
  async function onSubmit(event: React.FormEvent) {
    event.preventDefault()
    setIsLoading(true)
    
    // TODO: Implement password reset logic
    
    setIsLoading(false)
    setIsSent(true)
  }
  
  if (isSent) {
    return (
      <div className="text-center space-y-4">
        <Icons.check className="w-12 h-12 text-primary mx-auto" />
        <h2 className="text-xl font-semibold">
          Проверьте вашу почту
        </h2>
        <p className="text-muted-foreground">
          Мы отправили инструкции по восстановлению пароля на ваш email
        </p>
        <Button
          variant="link"
          onClick={() => router.push('/auth/login')}
        >
          Вернуться на страницу входа
        </Button>
      </div>
    )
  }
  
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="name@example.com"
          required
          disabled={isLoading}
        />
      </div>
      
      <Button className="w-full" disabled={isLoading}>
        {isLoading && (
          <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
        )}
        Отправить инструкции
      </Button>
      
      <p className="text-center text-sm text-muted-foreground">
        Вспомнили пароль?{' '}
        <Button
          variant="link"
          className="px-0"
          onClick={() => router.push('/auth/login')}
        >
          Войти
        </Button>
      </p>
    </form>
  )
} 
'use client';

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signIn } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Icons } from '@/components/ui/icons'
import { useTranslations } from 'next-intl'

export function LoginForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const t = useTranslations('Auth')
  
  async function onSubmit(event: React.FormEvent) {
    event.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      // Локальная авторизация через credentials
      const result = await signIn('credentials', { 
        redirect: false,
        email,
        password
      })
      
      if (result?.error) {
        setError(result.error)
      } else if (result?.ok) {
        router.push('/en/dashboard')
      }
    } catch (error) {
      console.error('Ошибка авторизации:', error)
      setError('Произошла ошибка при авторизации')
    } finally {
      setIsLoading(false)
    }
  }
  
  // Функция для авторизации через Keycloak (для демонстрации)
  const handleKeycloakLogin = async () => {
    setIsLoading(true)
    setError('')
    
    try {
      await signIn('keycloak', { 
        callbackUrl: window.location.origin + '/en/dashboard',
        redirect: true
      })
    } catch (error) {
      console.error('Ошибка авторизации через Keycloak:', error)
    }
  }
  
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      {error && (
        <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      <div className="space-y-2">
        <Label htmlFor="email">{t('email')}</Label>
        <Input
          id="email"
          type="email"
          placeholder="name@example.com"
          required
          disabled={isLoading}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      
      <div className="space-y-2">
        <Label htmlFor="password">{t('password')}</Label>
        <Input
          id="password"
          type="password"
          required
          disabled={isLoading}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Checkbox id="remember" />
          <Label htmlFor="remember" className="text-sm">
            {t('rememberMe')}
          </Label>
        </div>
        
        <Button
          variant="link"
          className="px-0 text-sm"
          onClick={() => router.push('/auth/forgot')}
        >
          {t('forgotPassword')}
        </Button>
      </div>
      
      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading && (
          <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
        )}
        {t('login')}
      </Button>
      
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            {t('loginWith')}
          </span>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <Button variant="outline" disabled={isLoading} onClick={handleKeycloakLogin}>
          <Icons.key className="mr-2 h-4 w-4" />
          Keycloak
        </Button>
        <Button variant="outline" disabled={isLoading}>
          <Icons.telegram className="mr-2 h-4 w-4" />
          Telegram
        </Button>
      </div>
      
      <p className="text-center text-sm text-muted-foreground">
        {t('dontHaveAccount')}{' '}
        <Button
          variant="link"
          className="px-0"
          onClick={() => router.push('/auth/register')}
        >
          {t('register')}
        </Button>
      </p>
    </form>
  )
} 
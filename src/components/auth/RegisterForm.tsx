'use client';

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signIn } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Select } from '@/components/ui/select'
import { Icons } from '@/components/ui/icons'
import { useTranslations } from 'next-intl'

const languages = [
  { value: 'ru', label: 'Русский' },
  { value: 'en', label: 'English' },
  { value: 'zh', label: '中文' }
]

export function RegisterForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [language, setLanguage] = useState('ru')
  const [error, setError] = useState('')
  const t = useTranslations('Auth')
  
  async function onSubmit(event: React.FormEvent) {
    event.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      // В реальном приложении здесь был бы API запрос для регистрации
      // Сейчас просто имитируем успешную регистрацию и авторизуем пользователя
      
      // Имитация задержки запроса
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // После "регистрации" сразу авторизуем пользователя
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
      console.error('Ошибка регистрации:', error)
      setError('Произошла ошибка при регистрации')
    } finally {
      setIsLoading(false)
    }
  }
  
  // Функция для регистрации через Keycloak (для демонстрации)
  const handleKeycloakRegister = async () => {
    setIsLoading(true)
    setError('')
    
    try {
      await signIn('keycloak', { 
        callbackUrl: window.location.origin + '/en/dashboard',
        redirect: true
      })
    } catch (error) {
      console.error('Ошибка регистрации через Keycloak:', error)
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
      
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="firstName">Имя</Label>
          <Input
            id="firstName"
            type="text"
            required
            disabled={isLoading}
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="lastName">Фамилия</Label>
          <Input
            id="lastName"
            type="text"
            required
            disabled={isLoading}
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>
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
      
      <div className="space-y-2">
        <Label htmlFor="language">Язык интерфейса</Label>
        <Select
          id="language"
          defaultValue="ru"
          disabled={isLoading}
          value={language}
          onValueChange={setLanguage}
        >
          {languages.map((lang) => (
            <option key={lang.value} value={lang.value}>
              {lang.label}
            </option>
          ))}
        </Select>
      </div>
      
      <div className="flex items-center space-x-2">
        <Checkbox id="terms" required />
        <Label htmlFor="terms" className="text-sm">
          {t('termsAgree')}{' '}
          <Button
            variant="link"
            className="px-0"
            onClick={() => router.push('/terms')}
          >
            условия использования
          </Button>
        </Label>
      </div>
      
      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading && (
          <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
        )}
        {t('register')}
      </Button>
      
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            {t('registerWith')}
          </span>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <Button variant="outline" disabled={isLoading} onClick={handleKeycloakRegister}>
          <Icons.key className="mr-2 h-4 w-4" />
          Keycloak
        </Button>
        <Button variant="outline" disabled={isLoading}>
          <Icons.telegram className="mr-2 h-4 w-4" />
          Telegram
        </Button>
      </div>
      
      <p className="text-center text-sm text-muted-foreground">
        {t('alreadyHaveAccount')}{' '}
        <Button
          variant="link"
          className="px-0"
          onClick={() => router.push('/auth/login')}
        >
          {t('login')}
        </Button>
      </p>
    </form>
  )
} 
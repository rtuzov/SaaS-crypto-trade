import { BILLING_INTERVAL, type PricingPlan } from '@/types/Subscription';

// FIXME: Update this configuration file based on your project information

export const localeConfig = {
  locales: ['en', 'ru', 'zh'] as const,
  defaultLocale: 'en' as const,
  localePrefix: 'always' as const,
} as const;

export type Locale = (typeof localeConfig.locales)[number];

export const AppConfig = {
  auth: {
    keycloak: {
      clientId: process.env.KEYCLOAK_CLIENT_ID || 'crypto-trade',
      clientSecret: process.env.KEYCLOAK_CLIENT_SECRET || 'your-client-secret',
      issuer: process.env.KEYCLOAK_ISSUER || 'http://localhost:8080/realms/crypto-trade',
    },
  },
  locales: [
    { id: 'en', name: 'English' },
    { id: 'ru', name: 'Русский' },
    { id: 'zh', name: '中文' },
  ],
  name: 'Crypto Trade',
  defaultLocale: 'en',
} as const;

export const PLAN_ID = {
  FREE: 'free',
  PREMIUM: 'premium',
  ENTERPRISE: 'enterprise',
} as const;

export const PricingPlanList: Record<string, PricingPlan> = {
  [PLAN_ID.FREE]: {
    id: PLAN_ID.FREE,
    price: 0,
    interval: BILLING_INTERVAL.MONTH,
    testPriceId: '',
    devPriceId: '',
    prodPriceId: '',
    features: {
      teamMember: 2,
      website: 2,
      storage: 2,
      transfer: 2,
    },
  },
  [PLAN_ID.PREMIUM]: {
    id: PLAN_ID.PREMIUM,
    price: 79,
    interval: BILLING_INTERVAL.MONTH,
    testPriceId: 'price_premium_test', // Use for testing
    // FIXME: Update the price ID, you can create it after running `npm run stripe:setup-price`
    devPriceId: 'price_1PNksvKOp3DEwzQlGOXO7YBK',
    prodPriceId: '',
    features: {
      teamMember: 5,
      website: 5,
      storage: 5,
      transfer: 5,
    },
  },
  [PLAN_ID.ENTERPRISE]: {
    id: PLAN_ID.ENTERPRISE,
    price: 199,
    interval: BILLING_INTERVAL.MONTH,
    testPriceId: 'price_enterprise_test', // Use for testing
    // FIXME: Update the price ID, you can create it after running `npm run stripe:setup-price`
    devPriceId: 'price_1PNksvKOp3DEwzQli9IvXzgb',
    prodPriceId: 'price_123',
    features: {
      teamMember: 100,
      website: 100,
      storage: 100,
      transfer: 100,
    },
  },
};

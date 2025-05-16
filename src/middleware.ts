import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

import { AppConfig, type Locale } from './utils/AppConfig';

const PUBLIC_ROUTES = [
  '/auth/login',
  '/auth/register',
  '/auth/reset-password',
  '/auth/error',
];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname.startsWith('/api/')
    || pathname.startsWith('/_next/')
    || pathname.startsWith('/static/')
    || pathname === '/favicon.ico') {
    return NextResponse.next();
  }

  if (pathname === '/') {
    return NextResponse.next();
  }

  const pathnameHasLocale = AppConfig.locales.some(
    locale => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`,
  );

  if (!pathnameHasLocale) {
    const locale = AppConfig.defaultLocale;
    return NextResponse.redirect(new URL(`/${locale}${pathname}`, request.url));
  }

  const isPublicRoute = PUBLIC_ROUTES.some(route =>
    pathname.endsWith(route) || pathname.includes(route),
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET,
    secureCookie: process.env.NODE_ENV === 'production',
  });

  if (!token && !isPublicRoute) {
    const locale = pathname.split('/')[1] as Locale;
    if (!AppConfig.locales.includes(locale)) {
      return NextResponse.redirect(new URL(`/${AppConfig.defaultLocale}/auth/login`, request.url));
    }
    const url = new URL(`/${locale}/auth/login`, request.url);
    url.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public/).*)',
  ],
};

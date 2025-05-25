import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import createMiddleware from 'next-intl/middleware';
import localeConfig from './next-intl.config.js';

const intlMiddleware = createMiddleware(localeConfig);

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  
  // Redirect root to default locale
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/en', request.url));
  }

  // Skip middleware for static files and API routes
  if (pathname.startsWith('/api/')
    || pathname.startsWith('/_next/')
    || pathname.startsWith('/static/')
    || pathname === '/favicon.ico') {
    return NextResponse.next();
  }
  return intlMiddleware(request);
}

export const config = {
  matcher: [
    '/((?!api|_next|.*\\..*).*)',
  ],
};

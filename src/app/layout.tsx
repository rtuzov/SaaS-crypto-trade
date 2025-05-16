import '@/styles/global.css';
import { ReactNode } from 'react';

export const metadata = { title: 'Crypto-SaaS' };

export default function Root({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useRef } from 'react';
import { Provider as UrqlProvider } from 'urql';

import { urqlClient } from '@/libs/graphqlClient';

export function ClientProviders({ children }: { children: React.ReactNode }) {
  const queryClientRef = useRef<QueryClient>();
  if (!queryClientRef.current) {
    queryClientRef.current = new QueryClient();
  }

  return (
    <QueryClientProvider client={queryClientRef.current}>
      <UrqlProvider value={urqlClient}>{children}</UrqlProvider>
    </QueryClientProvider>
  );
}

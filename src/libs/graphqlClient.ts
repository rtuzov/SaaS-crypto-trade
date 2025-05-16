import { cacheExchange, createClient, fetchExchange } from 'urql';

const GRAPHQL_URL = process.env.NEXT_PUBLIC_GRAPHQL_URL || 'http://localhost:4000/graphql';

export const urqlClient = createClient({
  url: GRAPHQL_URL,
  exchanges: [cacheExchange, fetchExchange],
  requestPolicy: 'cache-and-network',
  fetchOptions: () => {
    return {
      headers: {
        // Add any required headers here
      },
    };
  },
});

import { cacheExchange, createClient, fetchExchange, subscriptionExchange } from 'urql';
import { createClient as createWSClient } from 'graphql-ws';
import { gql } from '@urql/core';

const GRAPHQL_URL = process.env.NEXT_PUBLIC_GRAPHQL_URL || process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT || 'http://localhost:4000/graphql';
const GRAPHQL_WS_URL = process.env.NEXT_PUBLIC_GRAPHQL_WS || 'ws://localhost:8080/v1/graphql';

export const urqlClient = createClient({
  url: GRAPHQL_URL,
  exchanges: [
    cacheExchange,
    subscriptionExchange({
      forwardSubscription: (operation) => ({
        subscribe: (sink) =>
          createWSClient({
            url: GRAPHQL_WS_URL,
            retryAttempts: 5,
          }).subscribe(operation, sink),
      }),
    }),
    fetchExchange,
  ],
  requestPolicy: 'cache-and-network',
  fetchOptions: () => {
    return {
      headers: {
        'Content-Type': 'application/json',
      },
    };
  },
});

export const livePnlQuery = gql`
  query LivePnl {
    live_pnl {
      timestamp
      value
    }
  }
`;

import NextAuth from 'next-auth';
import KeycloakProvider from 'next-auth/providers/keycloak';
import CredentialsProvider from 'next-auth/providers/credentials';
import { JWT } from 'next-auth/jwt';
import { jwtDecode } from 'jwt-decode';

interface KeycloakToken {
  realm_access?: {
    roles: string[];
  };
  preferred_username?: string;
  email?: string;
  given_name?: string;
  family_name?: string;
}

// Временная база пользователей для демонстрации
const users = [
  {
    id: '1',
    email: 'user@example.com',
    password: 'password123',
    name: 'Test User',
    firstName: 'Test',
    lastName: 'User',
    roles: ['user']
  },
  {
    id: '2',
    email: 'admin@example.com',
    password: 'admin123',
    name: 'Admin User',
    firstName: 'Admin',
    lastName: 'User',
    roles: ['admin', 'user']
  }
];

const handler = NextAuth({
  providers: [
    // Добавляем локальную авторизацию через credentials
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        
        // Поиск пользователя в нашей временной базе
        const user = users.find(user => 
          user.email === credentials.email && 
          user.password === credentials.password
        );
        
        if (!user) return null;
        
        return {
          id: user.id,
          email: user.email,
          name: user.name,
          firstName: user.firstName,
          lastName: user.lastName,
          roles: user.roles
        };
      }
    }),
    // Оставляем Keycloak для интеграции
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_CLIENT_ID || 'trading-frontend',
      clientSecret: process.env.KEYCLOAK_CLIENT_SECRET || '',
      issuer: process.env.KEYCLOAK_ISSUER || 'http://localhost:8081/realms/trading-platform',
    }),
  ],
  callbacks: {
    async jwt({ token, account, user }) {
      // Добавляем данные из credentials провайдера
      if (user) {
        token.roles = user.roles;
        token.firstName = user.firstName;
        token.lastName = user.lastName;
      }
      
      // Добавляем данные из Keycloak
      if (account && account.access_token) {
        token.accessToken = account.access_token;
        token.refreshToken = account.refresh_token;
        token.idToken = account.id_token;
        token.expiresAt = account.expires_at;
        
        try {
          const decodedToken = jwtDecode<KeycloakToken>(account.access_token);
          if (decodedToken.realm_access?.roles) {
            token.roles = decodedToken.realm_access.roles;
          }
          if (decodedToken.preferred_username) {
            token.username = decodedToken.preferred_username;
          }
          if (decodedToken.given_name) {
            token.firstName = decodedToken.given_name;
          }
          if (decodedToken.family_name) {
            token.lastName = decodedToken.family_name;
          }
        } catch (error) {
          console.error('Ошибка декодирования токена:', error);
        }
      }
      
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      session.refreshToken = token.refreshToken;
      session.idToken = token.idToken;
      session.error = token.error;
      
      // Добавляем роли и дополнительные данные в сессию
      if (token.roles) {
        session.user.roles = token.roles;
      }
      if (token.username) {
        session.user.username = token.username;
      }
      if (token.firstName) {
        session.user.firstName = token.firstName;
      }
      if (token.lastName) {
        session.user.lastName = token.lastName;
      }
      
      return session;
    },
    async redirect({ url, baseUrl }) {
      // Убедимся, что перенаправление происходит только на наш домен
      if (url.startsWith(baseUrl)) return url;
      if (url.startsWith('/')) return `${baseUrl}${url}`;
      return baseUrl;
    }
  },
  pages: {
    signIn: '/auth/login',
    signOut: '/auth/logout',
    error: '/auth/error',
  },
  session: {
    strategy: 'jwt',
  },
});

// Export the handler for both GET and POST requests
export { handler as GET, handler as POST };

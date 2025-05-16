// src/types/next-auth.d.ts
import 'next-auth';

declare module 'next-auth' {
  type User = {
    id: string;
    role?: string;
  };

  type Session = {
    user: User & {
      name?: string | null;
      email?: string | null;
      image?: string | null;
    };
  };
}

declare module 'next-auth/jwt' {
  type JWT = {
    id: string;
    role?: string;
  };
}

import NextAuth from 'next-auth';

import { authOptions } from '@/libs/auth';

const handler = NextAuth(authOptions);

// Export the handler for both GET and POST requests
export { handler as GET, handler as POST };

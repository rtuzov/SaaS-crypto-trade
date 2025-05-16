'use client';
import { useParams, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';

export function withAuth(roles: string[]) {
  return function <P extends object>(Component: React.ComponentType<P>) {
    return (props: P) => {
      const { data: session, status } = useSession();
      const router = useRouter();
      const params = useParams();
      const locale = params.locale as string;

      if (status === 'loading') {
        return null;
      }

      const role = (session?.user as any)?.role;
      if (!session?.user || !roles.includes(role)) {
        router.replace(`/${locale}/auth/login`);
        return null;
      }
      return <Component {...props} />;
    };
  };
}

import Link from 'next/link';

export function Sidebar({ links }: { links: { href: string; label: string }[] }) {
  return (
    <aside className="w-48 border-r min-h-screen p-4 space-y-2">
      {links.map(({ href, label }) => (
        <Link
          key={href}
          href={href}
          className="block px-2 py-1 rounded hover:bg-muted transition-colors"
        >
          {label}
        </Link>
      ))}
    </aside>
  );
} 
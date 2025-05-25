import { Navigation } from './Navigation';
import { LocaleSwitcher } from './LocaleSwitcher';

export function Header() {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-40 w-full">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="text-lg font-semibold">TradingSaaS</div>
        <Navigation />
        <LocaleSwitcher />
      </div>
    </header>
  );
} 
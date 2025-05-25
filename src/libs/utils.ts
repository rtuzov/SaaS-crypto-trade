import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value: number): string {
  if (Math.abs(value) >= 1) {
    return value.toFixed(2);
  }
  
  const decimals = Math.abs(Math.log10(Math.abs(value)));
  return value.toFixed(Math.min(decimals + 2, 8));
}

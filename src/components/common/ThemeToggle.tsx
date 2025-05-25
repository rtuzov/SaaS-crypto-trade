"use client";
import { useTheme } from "next-themes";
import { Sun, Moon } from "lucide-react";
export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  return (
    <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="p-2 rounded-pill bg-primary/10">
      {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  );
} 
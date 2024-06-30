"use client";
import React, { createContext, useContext, useState, useEffect } from "react";
import { useTheme } from "next-themes";

interface ThemeContextType {
  theme: string;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const { theme: nextTheme, setTheme } = useTheme();
  const [theme, setLocalTheme] = useState<string>("light");

  useEffect(() => {
    setLocalTheme(nextTheme || "light");
  }, [nextTheme]);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useThemeContext must be used within a ThemeProvider");
  }
  return context;
};

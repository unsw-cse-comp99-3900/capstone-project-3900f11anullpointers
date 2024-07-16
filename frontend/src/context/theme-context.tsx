"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useTheme } from 'next-themes';

interface ThemeContextType {
  theme: string;
  textLarge: boolean;
  highContrast: boolean;
  dyslexicFont: boolean;
  toggleTheme: () => void;
  toggleTextSize: () => void;
  toggleHighContrast: () => void;
  toggleDyslexicFont: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const { theme: nextTheme, setTheme } = useTheme();
  const [theme, setLocalTheme] = useState<string>('light');
  const [textLarge, setTextLarge] = useState<boolean>(false);
  const [highContrast, setHighContrast] = useState<boolean>(false);
  const [dyslexicFont, setDyslexicFont] = useState<boolean>(false);

  useEffect(() => {
    setLocalTheme(nextTheme || 'light');
  }, [nextTheme]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const toggleTextSize = () => {
    setTextLarge(!textLarge);
    document.body.classList.toggle('text-large', !textLarge);
  };

  const toggleHighContrast = () => {
    setHighContrast(!highContrast);
    document.body.classList.toggle('high-contrast', !highContrast);
  };

  const toggleDyslexicFont = () => {
    setDyslexicFont(!dyslexicFont);
    document.body.classList.toggle('dyslexic-font', !dyslexicFont);
  };

  return (
    <ThemeContext.Provider value={{ theme, textLarge, highContrast, dyslexicFont, toggleTheme, toggleTextSize, toggleHighContrast, toggleDyslexicFont }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeContext must be used within a ThemeProvider');
  }
  return context;
};

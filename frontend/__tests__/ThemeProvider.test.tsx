import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import React, { useContext } from 'react';
import { ThemeProvider, useThemeContext } from '@/context/theme-context';
import { useTheme } from 'next-themes';

jest.mock('next-themes', () => ({
  useTheme: jest.fn(),
}));

const mockUseTheme = useTheme as jest.Mock;

describe('ThemeProvider', () => {
  beforeEach(() => {
    mockUseTheme.mockReturnValue({ theme: 'light', setTheme: jest.fn() });
  });

  const TestComponent = () => {
    const { theme, textLarge, highContrast, dyslexicFont, toggleTheme, toggleTextSize, toggleHighContrast, toggleDyslexicFont } = useThemeContext();
    return (
      <div>
        <div>Theme: {theme}</div>
        <div>Text Large: {textLarge.toString()}</div>
        <div>High Contrast: {highContrast.toString()}</div>
        <div>Dyslexic Font: {dyslexicFont.toString()}</div>
        <button onClick={toggleTheme}>Toggle Theme</button>
        <button onClick={toggleTextSize}>Toggle Text Size</button>
        <button onClick={toggleHighContrast}>Toggle High Contrast</button>
        <button onClick={toggleDyslexicFont}>Toggle Dyslexic Font</button>
      </div>
    );
  };

  it('provides default values from ThemeProvider', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    expect(screen.getByText('Theme: light')).toBeInTheDocument();
    expect(screen.getByText('Text Large: false')).toBeInTheDocument();
    expect(screen.getByText('High Contrast: false')).toBeInTheDocument();
    expect(screen.getByText('Dyslexic Font: false')).toBeInTheDocument();
  });

  it('toggles theme correctly', () => {
    const setThemeMock = jest.fn();
    mockUseTheme.mockReturnValue({ theme: 'light', setTheme: setThemeMock });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleThemeButton = screen.getByText('Toggle Theme');
    act(() => {
      toggleThemeButton.click();
    });

    expect(setThemeMock).toHaveBeenCalledWith('dark');
  });

  it('toggles text size correctly', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleTextSizeButton = screen.getByText('Toggle Text Size');
    act(() => {
      toggleTextSizeButton.click();
    });

    expect(screen.getByText('Text Large: true')).toBeInTheDocument();
    expect(document.body.classList.contains('text-large')).toBe(true);
  });

  it('toggles high contrast correctly', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleHighContrastButton = screen.getByText('Toggle High Contrast');
    act(() => {
      toggleHighContrastButton.click();
    });

    expect(screen.getByText('High Contrast: true')).toBeInTheDocument();
    expect(document.body.classList.contains('high-contrast')).toBe(true);
  });

  it('toggles dyslexic font correctly', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleDyslexicFontButton = screen.getByText('Toggle Dyslexic Font');
    act(() => {
      toggleDyslexicFontButton.click();
    });

    expect(screen.getByText('Dyslexic Font: true')).toBeInTheDocument();
    expect(document.body.classList.contains('dyslexic-font')).toBe(true);
  });
});

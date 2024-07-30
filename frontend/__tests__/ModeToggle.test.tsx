import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ModeToggle } from '@/components/ModeToggle'
import { ThemeProvider, useThemeContext } from '@/context/theme-context'

// Mock the useThemeContext hook
jest.mock('@/context/theme-context', () => ({
  useThemeContext: jest.fn(),
}))

const mockUseThemeContext = useThemeContext as jest.Mock

describe('ModeToggle component', () => {
  const mockToggleTheme = jest.fn()
  const mockToggleTextSize = jest.fn()
  const mockToggleHighContrast = jest.fn()
  const mockToggleDyslexicFont = jest.fn()

  const mockContextValue = {
    theme: 'light',
    textLarge: false,
    highContrast: false,
    dyslexicFont: false,
    toggleTheme: mockToggleTheme,
    toggleTextSize: mockToggleTextSize,
    toggleHighContrast: mockToggleHighContrast,
    toggleDyslexicFont: mockToggleDyslexicFont,
  }

  beforeEach(() => {
    mockUseThemeContext.mockReturnValue(mockContextValue)
    jest.clearAllMocks()
  })

  it('renders all toggle buttons', () => {
    render(
        <ModeToggle />
    )
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(4)
  })

  it('calls toggleTheme when the theme button is clicked', () => {
    render(
        <ModeToggle />
    )
    const themeToggleButton = screen.getByLabelText('Toggle theme')
    fireEvent.click(themeToggleButton)
    expect(mockToggleTheme).toHaveBeenCalledTimes(1)
  })

  it('calls toggleTextSize when the text size button is clicked', () => {
    render(
        <ModeToggle />
    )
    const textSizeToggleButton = screen.getByLabelText('Toggle large text')
    fireEvent.click(textSizeToggleButton)
    expect(mockToggleTextSize).toHaveBeenCalledTimes(1)
  })

  it('calls toggleHighContrast when the high contrast button is clicked', () => {
    render(
        <ModeToggle />
    )
    const highContrastToggleButton = screen.getByLabelText('Toggle high contrast')
    fireEvent.click(highContrastToggleButton)
    expect(mockToggleHighContrast).toHaveBeenCalledTimes(1)
  })

  it('calls toggleDyslexicFont when the dyslexic font button is clicked', () => {
    render(
        <ModeToggle />
    )
    const dyslexicFontToggleButton = screen.getByLabelText('Toggle dyslexic font')
    fireEvent.click(dyslexicFontToggleButton)
    expect(mockToggleDyslexicFont).toHaveBeenCalledTimes(1)
  })
})

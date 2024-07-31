import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { CardHeaderContent } from '@/components/CardHeaderContent'
import { useThemeContext } from '@/context/theme-context'

// Mock the useThemeContext hook
jest.mock('@/context/theme-context', () => ({
  useThemeContext: jest.fn(),
}))

const mockUseThemeContext = useThemeContext as jest.Mock

describe('CardHeaderContent component', () => {
  const mockContextValue = {
    textLarge: false,
    highContrast: false,
    dyslexicFont: false,
  }

  beforeEach(() => {
    mockUseThemeContext.mockReturnValue(mockContextValue)
  })

  it('renders the title and description', () => {
    const title = 'Test Title'
    const description = 'Test Description'
    render(
      <CardHeaderContent
        step={1}
        totalSteps={5}
        title={title}
        description={description}
      />
    )

    const titleElement = screen.getByText(title)
    const descriptionElement = screen.getByText(description)

    expect(titleElement).toBeInTheDocument()
    expect(descriptionElement).toBeInTheDocument()
  })

  it('applies the correct classes based on context values', () => {
    mockUseThemeContext.mockReturnValue({
      textLarge: true,
      highContrast: true,
      dyslexicFont: true,
    })

    const title = 'Test Title'
    const description = 'Test Description'
    render(
      <CardHeaderContent
        step={1}
        totalSteps={5}
        title={title}
        description={description}
      />
    )

    const titleElement = screen.getByText(title)
    const descriptionElement = screen.getByText(description)

    expect(titleElement).toHaveClass('text-5xl')
    expect(descriptionElement).toHaveClass('text-xl filter contrast-200')
  })
})

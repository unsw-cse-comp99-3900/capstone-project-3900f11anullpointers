// __tests__/Header.test.tsx
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import Header from '@/components/Header'
import { ThemeProvider } from '@/context/theme-context'

const BUTTONS_IN_MODE_TOGGLE = 4

describe('Header component', () => {
  it('renders the header with correct text', () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    )
    const heading = screen.getByText('UNSW Optometry Clinic')
    expect(heading).toBeInTheDocument()
  })

  it('renders the logo', () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    )
    const logo = screen.getByAltText('Logo')
    expect(logo).toBeInTheDocument()
  })

  it('renders the ModeToggle component', () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    )
    const toggleButtons = screen.getAllByRole('button')
    expect(toggleButtons).toHaveLength(BUTTONS_IN_MODE_TOGGLE)
  })
})

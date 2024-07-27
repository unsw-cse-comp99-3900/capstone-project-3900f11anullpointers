// src/__tests__/FormButtons.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { FormButtons } from '@/components/FormButtons';
import { useThemeContext } from '@/context/theme-context';
import { useFormContext } from 'react-hook-form';

// Mock the useThemeContext and useFormContext hooks
jest.mock('@/context/theme-context', () => ({
  useThemeContext: jest.fn(),
}));

jest.mock('react-hook-form', () => ({
  useFormContext: jest.fn(),
}));

const mockUseThemeContext = useThemeContext as jest.Mock;
const mockUseFormContext = useFormContext as jest.Mock;

describe('FormButtons component', () => {
  const mockContextValue = {
    textLarge: false,
    highContrast: false,
    dyslexicFont: false,
  };

  const mockFormContextValue = {
    trigger: jest.fn(),
    getValues: jest.fn(),
  };

  beforeEach(() => {
    mockUseThemeContext.mockReturnValue(mockContextValue);
    mockUseFormContext.mockReturnValue(mockFormContextValue);
  });

  const defaultProps = {
    formStep: 0,
    setFormStep: jest.fn(),
    isLoading: false,
    setIsLoading: jest.fn(),
    setIsSubmitted: jest.fn(),
    handleRestart: jest.fn(),
  };

  it('renders the "Next Page" button when formStep is 0', () => {
    render(<FormButtons {...defaultProps} formStep={0} />);
    const nextButton = screen.getByText('Next Page');
    expect(nextButton).toBeInTheDocument();
  });

  it('renders the "Go Back" and "Next Page" buttons when formStep is 1', () => {
    render(<FormButtons {...defaultProps} formStep={1} />);
    const goBackButton = screen.getByText('Go Back');
    const nextButton = screen.getByText('Next Page');
    expect(goBackButton).toBeInTheDocument();
    expect(nextButton).toBeInTheDocument();
  });

  it('renders the "Submit" button when formStep is 4', () => {
    render(<FormButtons {...defaultProps} formStep={4} />);
    const submitButton = screen.getByText('Submit');
    expect(submitButton).toBeInTheDocument();
  });

  it('renders the "Restart" button when formStep is 5', () => {
    render(<FormButtons {...defaultProps} formStep={5} />);
    const restartButton = screen.getByText('Restart');
    expect(restartButton).toBeInTheDocument();
  });
});

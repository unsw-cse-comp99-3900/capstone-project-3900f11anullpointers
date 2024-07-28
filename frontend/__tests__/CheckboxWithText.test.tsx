import React, { useEffect } from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { CheckboxWithText, CheckboxWithTextProps } from '@/components/CheckboxWithText';
import { useForm, FormProvider } from 'react-hook-form';
import { useThemeContext } from '@/context/theme-context';

// Mock the useThemeContext hook
jest.mock('@/context/theme-context', () => ({
  useThemeContext: jest.fn(),
}));

describe('CheckboxWithText', () => {
  const mockUseThemeContext = useThemeContext as jest.MockedFunction<typeof useThemeContext>;

  beforeEach(() => {
    mockUseThemeContext.mockReturnValue({
      textLarge: false,
      highContrast: false,
      dyslexicFont: false,
    });
  });

  const renderWithFormProvider = (props: CheckboxWithTextProps) => {
    const Wrapper: React.FC = ({ children }) => {
      return <FormProvider {...props.form}>{children}</FormProvider>;
    };

    return render(
      <FormProvider {...props.form}>
        <CheckboxWithText {...props} />
      </FormProvider>
    );
  };

  it('shows error message if there are consent errors', () => {
    const TestComponent = () => {
      const form = useForm({
        defaultValues: {
          acceptResearchConsent: false,
          denyResearchConsent: false,
          acceptContactConsent: false,
          denyContactConsent: false,
        },
      });

      useEffect(() => {
        form.setError('acceptResearchConsent', { type: 'manual', message: 'This field is required' });
        form.setError('denyResearchConsent', { type: 'manual', message: 'This field is required' });
      }, [form]);

      const props: CheckboxWithTextProps = {
        form,
        checkbox1: {
          name: 'acceptResearchConsent',
          labelText: 'Checkbox 1 Label',
          descriptionText: 'Checkbox 1 Description',
        },
        checkbox2: {
          name: 'denyResearchConsent',
          labelText: 'Checkbox 2 Label',
          descriptionText: 'Checkbox 2 Description',
        },
      };
      return (
        <FormProvider {...form}>
          <CheckboxWithText {...props} />
        </FormProvider>
      );
    };

    render(<TestComponent />);

    expect(screen.getByText('Please select ONE option.')).toBeInTheDocument();
  });
});

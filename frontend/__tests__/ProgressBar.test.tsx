import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ProgressBar from '@/components/ProgressBar';

describe('ProgressBar component', () => {
  it('renders the progress bar', () => {
    render(<ProgressBar step={1} totalSteps={5} />);
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toBeInTheDocument();
  });

  it('calculates the correct progress percentage', () => {
    render(<ProgressBar step={2} totalSteps={5} />);
    const progressDiv = screen.getByRole('progressbar').firstChild as HTMLElement;
    expect(progressDiv).toHaveStyle('width: 40%');
  });

  it('renders the progress bar with 0% progress when step is 0', () => {
    render(<ProgressBar step={0} totalSteps={5} />);
    const progressDiv = screen.getByRole('progressbar').firstChild as HTMLElement;
    expect(progressDiv).toHaveStyle('width: 0%');
  });

  it('renders the progress bar with 100% progress when step equals totalSteps', () => {
    render(<ProgressBar step={5} totalSteps={5} />);
    const progressDiv = screen.getByRole('progressbar').firstChild as HTMLElement;
    expect(progressDiv).toHaveStyle('width: 100%');
  });
});

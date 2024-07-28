import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Footer from '@/components/Footer';

describe('Footer component', () => {
  it('renders the footer with the correct text', () => {
    render(<Footer />);

    const footerText = screen.getByText('© 2024 UNSW');
    expect(footerText).toBeInTheDocument();
  });
});

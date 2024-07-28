// src/__tests__/TimeoutFeature.test.tsx
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import TimeoutFeature from '@/components/TimeoutFeature';

jest.useFakeTimers();

describe('TimeoutFeature component', () => {
  const resetTimers = () => {
    jest.runOnlyPendingTimers();
    jest.useFakeTimers();
  };

  beforeEach(() => {
    jest.clearAllTimers();
  });

  it('shows the inactivity prompt after 5 minutes of inactivity', async () => {
    render(<TimeoutFeature />);
    
    // Simulate 5 minutes of inactivity
    await act(() => {
      jest.advanceTimersByTime(300000);
    });
    
    const dialogTitle = await screen.findByText('Inactivity Alert');
    expect(dialogTitle).toBeInTheDocument();
    
    resetTimers();
  });

  it('resets the timer on user activity', async () => {
    render(<TimeoutFeature />);
    
    // Simulate 2 minutes of inactivity
    await act(() => {
      jest.advanceTimersByTime(120000);
    });
    
    // Simulate user activity
    await act(() => {
      fireEvent.mouseMove(window);
    });
    
    // Simulate another 2 minutes of inactivity
    await act(() => {
      jest.advanceTimersByTime(120000);
    });
    
    // The inactivity prompt should not be shown yet
    const dialogTitle = screen.queryByText('Inactivity Alert');
    expect(dialogTitle).not.toBeInTheDocument();
    
    // Simulate additional 3 minutes of inactivity (total 5 minutes)
    await act(() => {
      jest.advanceTimersByTime(180000);
    });
    
    const dialogTitleAfterTimeout = await screen.findByText('Inactivity Alert');
    expect(dialogTitleAfterTimeout).toBeInTheDocument();
    
    resetTimers();
  });

  it('extends the session when "Extend" button is clicked', async () => {
    render(<TimeoutFeature />);
    
    // Simulate 5 minutes of inactivity
    act(() => {
      jest.advanceTimersByTime(300000);
    });
    
    const dialogTitle = await screen.findByText('Inactivity Alert');
    expect(dialogTitle).toBeInTheDocument();
    
    const extendButton = screen.getByText('Extend');
    act(() => {
      fireEvent.click(extendButton);
    });
    
    // The inactivity prompt should be closed
    await waitFor(() => {
      expect(screen.queryByText('Inactivity Alert')).not.toBeInTheDocument();
    });
    
    // Simulate additional 5 minutes of inactivity
    act(() => {
      jest.advanceTimersByTime(300000);
    });
    
    const dialogTitleAfterExtension = await screen.findByText('Inactivity Alert');
    expect(dialogTitleAfterExtension).toBeInTheDocument();
    
    resetTimers();
  });

  it('resets the form after 15 seconds of showing the prompt', async () => {
    render(<TimeoutFeature />);
    
    // Simulate 5 minutes of inactivity
    act(() => {
      jest.advanceTimersByTime(300000);
    });
    
    const dialogTitle = await screen.findByText('Inactivity Alert');
    expect(dialogTitle).toBeInTheDocument();
    
    // Simulate 15 seconds of inactivity after showing the prompt
    act(() => {
      jest.advanceTimersByTime(15000);
    });
    
    // The inactivity prompt should be closed and form should be reset
    await waitFor(() => {
      expect(screen.queryByText('Inactivity Alert')).not.toBeInTheDocument();
    });
    
    resetTimers();
  });
});

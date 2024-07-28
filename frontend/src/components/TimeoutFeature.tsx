import React, { useState, useEffect, useRef } from 'react';
import { useTheme } from 'next-themes';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button";

const TimeoutFeature = () => {
  const [isIdle, setIsIdle] = useState(false);
  const [showPrompt, setShowPrompt] = useState(false);
  const timeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);
  const promptTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { theme } = useTheme();

  // Reset timers
  const resetTimer = () => {
    if (timeoutId.current) clearTimeout(timeoutId.current);
    if (promptTimeoutId.current) clearTimeout(promptTimeoutId.current);

    // Set the timeout to show the prompt after 5 minutes
    timeoutId.current = setTimeout(() => {
      setIsIdle(true);
      setShowPrompt(true);

      // Start the timeout for the prompt
      promptTimeoutId.current = setTimeout(() => {
        setShowPrompt(false);
        window.location.href = window.location.href; // Refresh the page
      }, 15000); // 15 seconds to press the "Extend" button
    }, 300000); // 5 minutes before showing the prompt
  };

  // Handle Extend button click
  const handleExtend = () => {
    setIsIdle(false);
    setShowPrompt(false);
    resetTimer();
  };

  // Handle user activity
  const handleUserActivity = () => {
    resetTimer();
  };

  useEffect(() => {
    // Event listeners to track user activity
    window.addEventListener('touchstart', handleUserActivity);
    window.addEventListener('touchmove', handleUserActivity);
    window.addEventListener('keydown', handleUserActivity);
    window.addEventListener('scroll', handleUserActivity);
    window.addEventListener('mousemove', handleUserActivity);

    resetTimer();

    // Clean up listeners
    return () => {
      window.removeEventListener('touchstart', handleUserActivity);
      window.removeEventListener('touchmove', handleUserActivity);
      window.removeEventListener('keydown', handleUserActivity);
      window.removeEventListener('scroll', handleUserActivity);
      window.removeEventListener('mousemove', handleUserActivity);
      if (timeoutId.current) clearTimeout(timeoutId.current);
      if (promptTimeoutId.current) clearTimeout(promptTimeoutId.current);
    };
  }, []);

  return (
    <div>
      {showPrompt && isIdle && (
        <Dialog open={showPrompt} onOpenChange={setShowPrompt}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Inactivity Alert</DialogTitle>
              <DialogDescription>
                You have been inactive for five minutes. Please press "Extend" to continue your session, or the form will reset.
              </DialogDescription>
            </DialogHeader>
              <Button onClick={handleExtend}>Extend</Button>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default TimeoutFeature;

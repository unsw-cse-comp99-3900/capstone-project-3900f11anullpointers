import React, { createContext, useState, useEffect, useContext } from 'react';
import IdleScreen from './IdleScreen';

const IdleContext = createContext();

export const useIdle = () => useContext(IdleContext);

const IdleDetectionProvider = ({ children, resetToHome }) => {
  const [isIdle, setIsIdle] = useState(false);
  const [isIdleScreenVisible, setIsIdleScreenVisible] = useState(false);
  const [countdown, setCountdown] = useState(5); // 5 seconds for the countdown
  const idleTime = 5000; // 5 seconds

  useEffect(() => {
    let idleTimer;
    let idleScreenTimer;
    let countdownInterval;

    const resetTimer = () => {
      clearTimeout(idleTimer);
      clearTimeout(idleScreenTimer);
      clearInterval(countdownInterval);
      setIsIdle(false);
      setIsIdleScreenVisible(false);
      setCountdown(5);
      idleTimer = setTimeout(() => handleUserBecomesIdle(), idleTime);
    };

    const handleUserBecomesIdle = () => {
      setIsIdle(true);
      setIsIdleScreenVisible(true);
      countdownInterval = setInterval(() => {
        setCountdown(prevCountdown => {
          if (prevCountdown <= 1) {
            clearInterval(countdownInterval);
            setIsIdleScreenVisible(false); // Hide the idle screen
            resetToHome();
            return 5;
          }
          return prevCountdown - 1;
        });
      }, 1000); // Decrement countdown every second
    };

    // Computer
    window.addEventListener('mousemove', resetTimer);
    window.addEventListener('keydown', resetTimer);
    window.addEventListener('scroll', resetTimer);

    // Ipad
    window.addEventListener('touchstart', resetTimer);
    window.addEventListener('touchmove', resetTimer);

    // Set the initial timer
    idleTimer = setTimeout(handleUserBecomesIdle, idleTime);

    return () => {
      clearTimeout(idleTimer);
      clearTimeout(idleScreenTimer);
      clearInterval(countdownInterval);
      window.removeEventListener('mousemove', resetTimer);
      window.removeEventListener('keydown', resetTimer);
      window.removeEventListener('scroll', resetTimer);
      window.removeEventListener('touchstart', resetTimer);
      window.removeEventListener('touchmove', resetTimer);
    };
  }, [idleTime, resetToHome]);

  return (
    <IdleContext.Provider value={{ isIdle }}>
      {isIdleScreenVisible && <IdleScreen countdown={countdown} />}
      {children}
    </IdleContext.Provider>
  );
};

export default IdleDetectionProvider;

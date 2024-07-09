import React from 'react';

const IdleScreen = ({ countdown }) => {
  return (
    <div style={styles.idleScreen}>
        <h1>You have been inactive for a while</h1>
        <h1>The form will reset in {countdown} second{countdown !== 1 ? 's' : ''}</h1>
        <p>Tap anywhere to cancel</p>
    </div>
  );
};

const styles = {
  idleScreen: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    color: '#fff',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
};

export default IdleScreen;
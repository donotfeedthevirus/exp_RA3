const servoForm = document.getElementById('servo-form');
if (servoForm) {
  servoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const angle = document.getElementById('angle').value;
    console.log(`Sending servo angle: ${angle}`);

    try {
      const response = await fetch('/api/servo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ angle })
      });
      const result = await response.json();
      alert(`Servo angle set to ${result.angle}`);
    } catch (err) {
      console.error('Error setting servo:', err);
      alert('Failed to set servo');
    }
  });
}

const buzzerForm = document.getElementById('buzzer-form');
if (buzzerForm) {
  buzzerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const frequency = document.getElementById('frequency').value;
    const volume = document.getElementById('volume').value;
    console.log(`Sending buzzer settings: freq=${frequency}, vol=${volume}`);

    try {
      const response = await fetch('/api/buzzer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frequency, volume })
      });
      const result = await response.json();
      alert(`Buzzer set: freq=${frequency}Hz, volume=${volume}`);
    } catch (err) {
      console.error('Error setting buzzer:', err);
      alert('Failed to set buzzer');
    }
  });
}

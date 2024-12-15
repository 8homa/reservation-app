async function makeReservation() {
  const date = document.getElementById('date').value;
  const time = document.getElementById('time').value;
  const user = document.getElementById('user').value;

  if (!date || !time || !user) {
    showMessage('すべての項目を入力してください。');
    return;
  }

  try {
    const response = await fetch('/reservations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, user })
    });

    const result = await response.json();

    if (response.ok) {
      showMessage(result.message, true);
    } else {
      showMessage(result.error || 'エラーが発生しました。');
    }
  } catch (err) {
    showMessage('サーバーに接続できません。');
  }
}

function showMessage(message, success = false) {
  const messageEl = document.getElementById('message');
  messageEl.textContent = message;
  messageEl.style.color = success ? 'green' : 'red';
}

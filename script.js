const form = document.getElementById('checkin-form');
const nameInput = document.getElementById('name');
const targetLatInput = document.getElementById('targetLat');
const targetLngInput = document.getElementById('targetLng');
const radiusInput = document.getElementById('radius');
const statusEl = document.getElementById('status');
const historyList = document.getElementById('history-list');

function setStatus(message, type = 'info') {
  statusEl.textContent = message;
  statusEl.className = `status ${type}`;
}

function getHistory() {
  try {
    return JSON.parse(localStorage.getItem('location-checkins') || '[]');
  } catch (error) {
    return [];
  }
}

function saveHistory(records) {
  localStorage.setItem('location-checkins', JSON.stringify(records));
}

function formatDistance(distance) {
  if (distance < 1000) {
    return `${Math.round(distance)} เมตร`;
  }
  return `${(distance / 1000).toFixed(2)} กม.`;
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleString('th-TH', {
    dateStyle: 'medium',
    timeStyle: 'short'
  });
}

function toRad(value) {
  return (value * Math.PI) / 180;
}

function calculateDistance(lat1, lon1, lat2, lon2) {
  const earthRadius = 6371000;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return earthRadius * c;
}

function renderHistory() {
  const records = getHistory();

  if (!records.length) {
    historyList.innerHTML = '<li>ยังไม่มีประวัติการเช็กชื่อ</li>';
    return;
  }

  historyList.innerHTML = records.slice(0, 8).map((record) => {
    const statusText = record.status === 'inside' ? 'ผ่าน' : 'อยู่นอกพื้นที่';
    return `
      <li>
        <strong>${record.name}</strong>
        <span>${statusText}</span>
        <small>${formatTime(record.timestamp)}</small>
      </li>
    `;
  }).join('');
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = nameInput.value.trim();
  const targetLat = parseFloat(targetLatInput.value);
  const targetLng = parseFloat(targetLngInput.value);
  const radius = parseFloat(radiusInput.value);

  if (!name) {
    setStatus('กรุณากรอกชื่อก่อนเช็กชื่อ', 'error');
    return;
  }

  if (Number.isNaN(targetLat) || Number.isNaN(targetLng) || Number.isNaN(radius)) {
    setStatus('กรุณากรอกพิกัดเป้าหมายและรัศมีให้ถูกต้อง', 'error');
    return;
  }

  setStatus('กำลังขอสิทธิ์เข้าถึงตำแหน่งของคุณ...', 'info');

  if (!navigator.geolocation) {
    setStatus('เบราว์เซอร์ของคุณไม่รองรับการใช้ตำแหน่ง', 'error');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const distance = calculateDistance(
        position.coords.latitude,
        position.coords.longitude,
        targetLat,
        targetLng
      );
      const isInside = distance <= radius;
      const records = getHistory();
      const newRecord = {
        name,
        distance,
        status: isInside ? 'inside' : 'outside',
        timestamp: new Date().toISOString()
      };

      records.unshift(newRecord);
      records.splice(8);
      saveHistory(records);
      renderHistory();

      if (isInside) {
        setStatus(`${name} เช็กชื่อสำเร็จ! คุณอยู่ในพื้นที่ห่าง ${formatDistance(distance)} จากจุดเป้าหมาย`, 'success');
      } else {
        setStatus(`${name} ยังอยู่นอกพื้นที่ โดยห่างจากจุดเป้าหมาย ${formatDistance(distance)}`, 'error');
      }
    },
    () => {
      setStatus('ไม่สามารถเข้าถึงตำแหน่งของคุณได้ กรุณาเปิดสิทธิ์ Location ในเบราว์เซอร์', 'error');
    },
    {
      enableHighAccuracy: true,
      timeout: 10000
    }
  );
});

renderHistory();

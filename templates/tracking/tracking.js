const ORDER_ID = "12345";
const API_URL = `http://localhost:8000/api/tracking/orders/${ORDER_ID}/`;

document.getElementById("order-id").innerText = ORDER_ID;

const map = L.map("map").setView([-33.45, -70.66], 14);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let marker = L.marker([-33.45, -70.66]).addTo(map);

async function fetchLocation() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    document.getElementById("status").innerText = data.status || "-";

    if (!data.location) return;

    const lat = parseFloat(data.location.latitude);
    const lng = parseFloat(data.location.longitude);

    marker.setLatLng([lat, lng]);
    map.setView([lat, lng]);

    document.getElementById("timestamp").innerText = data.location.timestamp;
  } catch {
    console.log("Error obteniendo ubicación");
  }
}

fetchLocation();
setInterval(fetchLocation, 5000);

const ORDER_ID = "12345";
const API_URL = `http://localhost:8000/api/tracking/orders/${ORDER_ID}/`;

document.getElementById("order-id").innerText = ORDER_ID;

// --- Inicialización del mapa ---
const map = L.map("map", { zoomControl: true }).setView([-33.45, -70.66], 14);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
}).addTo(map);

// Marcador personalizado (color azul estilo tracking)
let marker = L.marker([-33.45, -70.66], {
    riseOnHover: true
}).addTo(map);

// Lista de puntos para la ruta
let routePoints = [];
let routeLine = L.polyline([], { color: "#3498db", weight: 4 }).addTo(map);

// Tabla de colores por estado
const STATUS_COLORS = {
    "pendiente": "#f39c12",
    "en_camino": "#2980b9",
    "entregado": "#27ae60",
    "cancelado": "#c0392b"
};

function updateStatusColor(statusText) {
    const statusEl = document.getElementById("status");
    statusEl.innerText = statusText || "-";

    const color = STATUS_COLORS[statusText] || "#2e7d32";
    statusEl.style.background = color + "20"; // transparente
    statusEl.style.color = color;
}

// --- Animación suave entre posiciones ---
function animateMarker(oldLatLng, newLatLng, duration = 800) {
    const start = performance.now();

    function frame(now) {
        const progress = Math.min((now - start) / duration, 1);

        const lat = oldLatLng.lat + (newLatLng.lat - oldLatLng.lat) * progress;
        const lng = oldLatLng.lng + (newLatLng.lng - oldLatLng.lng) * progress;

        marker.setLatLng([lat, lng]);

        if (progress < 1) {
            requestAnimationFrame(frame);
        }
    }

    requestAnimationFrame(frame);
}

// --- Función principal ---
async function fetchLocation() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        // Actualizar estado visualmente
        updateStatusColor(data.status);

        if (!data.location) return;

        const lat = parseFloat(data.location.latitude);
        const lng = parseFloat(data.location.longitude);
        const newLatLng = L.latLng(lat, lng);
        const oldLatLng = marker.getLatLng();

        // Animación del marcador
        animateMarker(oldLatLng, newLatLng);

        // Animación del mapa hacia la nueva posición
        map.flyTo(newLatLng, map.getZoom(), { duration: 0.6 });

        // Agregar punto a la ruta
        routePoints.push(newLatLng);
        routeLine.setLatLngs(routePoints);

        // Actualizar timestamp
        document.getElementById("timestamp").innerText =
            data.location.timestamp || "-";

    } catch (error) {
        console.error("Error obteniendo ubicación:", error);
    }
}

// Primera carga
fetchLocation();

// Actualizar cada 5 segundos
setInterval(fetchLocation, 5000);

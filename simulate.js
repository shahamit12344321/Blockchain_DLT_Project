/**
 * IoT/GPS Shipment Event Simulator
 *
 * Simulates 5 shipments moving along realistic Indian transport corridors with:
 * - Incremental lat/lng movement along waypoints
 * - Realistic temperature + humidity fluctuations
 * - Occasional anomalies: temperature spikes, highway stops, cold-chain excursions
 *
 * Run: node simulator/simulate.js
 */

const http = require('http');

const PORT = process.env.PORT || 4001;
const API_BASE = process.env.API_BASE || `http://localhost:${PORT}`;
const INTERVAL_MS = 4000; // new event every 4 seconds

// ── Shipment Route Definitions ── Indian Highway Corridors ───────────────────
const SHIPMENTS = [
  {
    id: 'SHP-001',
    name: 'Electronics – Chennai to Delhi',
    carrier: 'Blue Dart Express',
    waypoints: [
      [13.08, 80.27],   // Chennai
      [14.93, 78.82],   // Cuddapah
      [15.82, 78.03],   // Kurnool
      [17.38, 78.49],   // Hyderabad
      [19.07, 80.05],   // Nagpur (via NH-44)
      [23.18, 77.41],   // Bhopal
      [26.45, 80.35],   // Kanpur
      [28.70, 77.10],   // New Delhi
    ],
    baseTemp: 28, tempRange: 4,
    baseHumidity: 60, humidityRange: 10,
    eventTypes: ['location_update', 'location_update', 'location_update', 'checkpoint'],
    anomalyChance: 0.07,
  },
  {
    id: 'SHP-002',
    name: 'Pharma Cold Chain – Mumbai to Kolkata',
    carrier: 'TCI Cold Chain',
    waypoints: [
      [19.07, 72.87],   // Mumbai
      [19.99, 73.78],   // Nashik
      [21.44, 73.01],   // Surat
      [22.71, 75.85],   // Indore
      [23.18, 79.98],   // Jabalpur
      [21.15, 81.63],   // Raipur
      [20.27, 85.84],   // Bhubaneswar
      [22.57, 88.36],   // Kolkata
    ],
    baseTemp: 5.0, tempRange: 1.5,  // Strict cold chain (2°C–8°C)
    baseHumidity: 72, humidityRange: 5,
    eventTypes: ['location_update', 'location_update', 'checkpoint'],
    anomalyChance: 0.15, // 15% excursion injection for demonstration
  },
  {
    id: 'SHP-003',
    name: 'Textile Export – Surat to JNPT Port',
    carrier: 'Maersk India',
    waypoints: [
      [21.17, 72.83],   // Surat
      [21.65, 73.30],   // Navsari
      [20.90, 73.00],   // Valsad
      [20.42, 72.92],   // Palghar
      [19.42, 72.83],   // Vasai
      [18.95, 72.94],   // Navi Mumbai / JNPT
    ],
    baseTemp: 31, tempRange: 3,
    baseHumidity: 65, humidityRange: 12,
    eventTypes: ['location_update', 'location_update', 'checkpoint'],
    anomalyChance: 0.05,
  },
  {
    id: 'SHP-004',
    name: 'Auto Parts – Pune to Bengaluru',
    carrier: 'V-Trans Logistics',
    waypoints: [
      [18.52, 73.85],   // Pune
      [17.68, 74.00],   // Satara
      [16.70, 74.24],   // Kolhapur
      [15.84, 74.49],   // Belagavi
      [15.36, 75.12],   // Hubballi
      [14.46, 75.92],   // Davanagere
      [13.34, 77.10],   // Tumakuru
      [12.97, 77.59],   // Bengaluru
    ],
    baseTemp: 27, tempRange: 3.5,
    baseHumidity: 55, humidityRange: 8,
    eventTypes: ['location_update', 'location_update', 'location_update', 'checkpoint'],
    anomalyChance: 0.08,
  },
  {
    id: 'SHP-005',
    name: 'FMCG Consumer Goods – Ahmedabad to Guwahati',
    carrier: 'Delhivery Surface',
    waypoints: [
      [23.02, 72.57],   // Ahmedabad
      [24.58, 73.71],   // Udaipur
      [26.91, 75.78],   // Jaipur
      [27.18, 78.00],   // Agra
      [26.84, 80.94],   // Lucknow
      [25.59, 85.13],   // Patna
      [26.72, 88.39],   // Siliguri
      [26.14, 91.73],   // Guwahati
    ],
    baseTemp: 29, tempRange: 4,
    baseHumidity: 58, humidityRange: 10,
    eventTypes: ['location_update', 'location_update', 'location_update', 'checkpoint'],
    anomalyChance: 0.10,
  },
];

// In-memory simulation states per shipment
const states = SHIPMENTS.map((s, idx) => ({
  shipment: s,
  waypointIndex: 0,
  stepProgress: (idx * 0.15) % 0.8, // stagger start progress
  speed_kmh: 55,
}));

function jitter(range) {
  return (Math.random() - 0.5) * range;
}

function interpolate(p1, p2, frac) {
  return [
    p1[0] + (p2[0] - p1[0]) * frac,
    p1[1] + (p2[1] - p1[1]) * frac,
  ];
}

function postEvent(payload) {
  const data = JSON.stringify(payload);
  const url = new URL(`${API_BASE}/api/events`);

  const options = {
    hostname: url.hostname,
    port:     url.port || (url.protocol === 'https:' ? 443 : 80),
    path:     url.pathname,
    method:   'POST',
    headers:  {
      'Content-Type':   'application/json',
      'Content-Length': Buffer.byteLength(data),
    },
    timeout: 3000,
  };

  const req = http.request(options, (res) => {
    // Consume response
    res.on('data', () => {});
  });

  req.on('error', (err) => {
    // Backend may be starting up
    if (err.code !== 'ECONNREFUSED') {
      console.warn(`[Simulator Warning] POST /api/events: ${err.message}`);
    }
  });

  req.write(data);
  req.end();
}

function stepShipment(st) {
  const { shipment } = st;
  const wps = shipment.waypoints;

  // Advance along current segment
  st.stepProgress += 0.08 + Math.random() * 0.05;
  if (st.stepProgress >= 1.0) {
    st.stepProgress = 0;
    st.waypointIndex++;
    if (st.waypointIndex >= wps.length - 1) {
      // Loop back for continuous live demo
      st.waypointIndex = 0;
    }
  }

  const p1 = wps[st.waypointIndex];
  const p2 = wps[st.waypointIndex + 1];
  const [lat, lng] = interpolate(p1, p2, st.stepProgress);

  // Overall progress percentage
  const totalSegments = wps.length - 1;
  const currentTotalProgress = (st.waypointIndex + st.stepProgress) / totalSegments;
  const progressPct = Math.min(Math.round(currentTotalProgress * 100), 99);

  // Temperature with realistic jitter and anomaly injection
  let isAnomaly = Math.random() < shipment.anomalyChance;
  let temp = shipment.baseTemp + jitter(shipment.tempRange);
  let humidity = Math.round(shipment.baseHumidity + jitter(shipment.humidityRange));

  if (isAnomaly) {
    if (shipment.id === 'SHP-002') {
      // Cold-chain excursion: Spike to 9.5°C - 14.0°C (threshold is 8.0°C)
      temp += 5.5 + Math.random() * 6.0;
    } else {
      // General cargo thermal excursion
      temp += 8.0 + Math.random() * 8.0;
    }
  }
  temp = parseFloat(temp.toFixed(1));

  // Speed and event type
  let speed = 45 + Math.round(Math.random() * 25);
  let eventType = shipment.eventTypes[Math.floor(Math.random() * shipment.eventTypes.length)];
  let notes = 'Normal transit telemetry update';

  if (isAnomaly) {
    if (Math.random() < 0.4) {
      speed = 0; // Unplanned highway halt
      notes = 'Unplanned stoppage / traffic congestion on highway';
    } else {
      notes = 'Sensor anomaly detected: Temperature excursion outside nominal SLA';
    }
  }

  const payload = {
    shipment_id: shipment.id,
    lat:         parseFloat(lat.toFixed(4)),
    lng:         parseFloat(lng.toFixed(4)),
    temperature: temp,
    humidity:    humidity,
    speed_kmh:   speed,
    status:      speed === 0 ? 'Delayed' : 'In Transit',
    event_type:  eventType,
    notes:       notes,
    progress:    progressPct,
  };

  postEvent(payload);

  const anomalyTag = isAnomaly ? ` \x1b[31m[ANOMALY: ${temp}°C]\x1b[0m` : '';
  console.log(
    `[Simulator] ${shipment.id} (${shipment.carrier}) -> (${payload.lat}, ${payload.lng}) | ${temp}°C | ${speed} km/h | ${progressPct}%${anomalyTag}`
  );
}

console.log(`\n🚚 [Simulator] Starting IoT Telemetry for 5 Shipments...`);
console.log(`   Target Endpoint: ${API_BASE}/api/events`);
console.log(`   Interval: ${INTERVAL_MS / 1000}s per batch\n`);

// Run first step immediately
states.forEach(stepShipment);

// Recurring pulse
setInterval(() => {
  states.forEach(stepShipment);
}, INTERVAL_MS);
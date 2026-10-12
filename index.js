const express   = require('express');
const http      = require('http');
const WebSocket = require('ws');
const path      = require('path');
const db        = require('./db');
const { predictAllShipments } = require('./ml-predictor');
const { getChain, verifyChain, addCheckpoint, tamperBlock, restoreTamperedBlock } = require('./blockchain-ledger');
const { checkStaleShipments, checkExceptions } = require('./exception-engine');
const { router: eventsRouter, setBroadcast } = require('./routes/events');

const app    = express();
const server = http.createServer(app);
const wss    = new WebSocket.Server({ server });

app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'public')));

// ── WebSocket broadcast ───────────────────────────────────────────────────────
const clients = new Set();

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log(`[WS] Client connected. Total: ${clients.size}`);

  // Send initial KPI update
  try {
    ws.send(JSON.stringify({ event: 'kpi_update', data: db.kpis() }));
  } catch (e) {}

  ws.on('close', () => {
    clients.delete(ws);
    console.log(`[WS] Client disconnected. Total: ${clients.size}`);
  });
});

function broadcast(msg) {
  const str = JSON.stringify(msg);
  for (const ws of clients) {
    if (ws.readyState === WebSocket.OPEN) {
      try {
        ws.send(str);
      } catch (e) {}
    }
  }
}

setBroadcast(broadcast);

// ── REST API Routes ───────────────────────────────────────────────────────────
app.use('/api/events', eventsRouter);

// Shipments
app.get('/api/shipments', (req, res) => {
  res.json(db.getShipments());
});

app.get('/api/shipments/:id', (req, res) => {
  const s = db.getShipment(req.params.id);
  if (!s) return res.status(404).json({ error: 'Shipment not found' });
  const events = db.getEvents(s.id, 25);
  const alerts = db.getAlertsByShipment(s.id);
  res.json({ ...s, recent_events: events, alerts });
});

// Alerts
app.get('/api/alerts', (req, res) => {
  const resolved = req.query.resolved !== undefined ? parseInt(req.query.resolved) : 0;
  const limit    = parseInt(req.query.limit) || 100;
  res.json(db.getAlerts(resolved, limit));
});

app.patch('/api/alerts/:id/resolve', (req, res) => {
  const ok = db.resolveAlert(req.params.id);
  if (ok) {
    broadcast({ event: 'alert_resolved', data: { id: parseInt(req.params.id) } });
    broadcast({ event: 'kpi_update', data: db.kpis() });
    res.json({ success: true, message: 'Alert resolved' });
  } else {
    res.status(404).json({ error: 'Alert not found or already resolved' });
  }
});

// Analytics & Reports
app.get('/api/analytics/kpis', (req, res) => {
  res.json(db.kpis());
});

app.get('/api/analytics/predictions', (req, res) => {
  res.json(predictAllShipments());
});

app.get('/api/analytics/ledger', (req, res) => {
  const limit = parseInt(req.query.limit) || 30;
  const chain = getChain(limit);
  const audit = verifyChain();
  res.json({ chain, ...audit });
});

app.get('/api/analytics/carriers', (req, res) => {
  res.json(db.carrierPerf());
});

app.get('/api/analytics/temp-history/:shipmentId', (req, res) => {
  res.json(db.tempHistory(req.params.shipmentId));
});

app.get('/api/analytics/frequency', (req, res) => {
  res.json(db.eventFrequency());
});

app.get('/api/analytics/alert-trend', (req, res) => {
  res.json(db.alertTrend());
});

// CSV Export for Faculty Viva
app.get('/api/analytics/export/csv', (req, res) => {
  const shipments = db.getShipments();
  let events = [];
  shipments.forEach(s => {
    events = events.concat(db.getEvents(s.id, 500));
  });
  let csv = 'ID,Shipment_ID,Timestamp,Latitude,Longitude,Temperature_C,Humidity_Pct,Speed_KMH,Status,Event_Type,Notes\n';
  events.forEach(e => {
    csv += `${e.id},${e.shipment_id},${e.timestamp},${e.lat},${e.lng},${e.temperature},${e.humidity},${e.speed_kmh},"${e.status}","${e.event_type}","${(e.notes || '').replace(/"/g, '""')}"\n`;
  });
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename="ChainVision_Telemetry_Log.csv"');
  res.send(csv);
});

// ── Interactive Viva Demonstration Endpoints ─────────────────────────────────
app.post('/api/ledger/tamper', (req, res) => {
  const result = tamperBlock(req.body.id, req.body.data);
  if (!result) return res.status(404).json({ error: 'Block not found' });
  const audit = verifyChain();
  broadcast({ event: 'ledger_update', data: { tampered: true, ...audit } });
  res.json({ message: 'Cryptographic block altered for tampering simulation', ...result, ...audit });
});

app.post('/api/ledger/restore', (req, res) => {
  const ok = restoreTamperedBlock();
  const audit = verifyChain();
  broadcast({ event: 'ledger_update', data: { restored: ok, ...audit } });
  res.json({ success: ok, message: 'Ledger integrity cryptographically restored', ...audit });
});

app.post('/api/simulate/trigger', (req, res) => {
  const { scenario } = req.body;
  if (scenario === 'cold_chain_spike') {
    const s = db.getShipment('SHP-002');
    if (s) {
      const ev = db.insertEvent({
        shipment_id: 'SHP-002',
        lat: s.lat, lng: s.lng,
        temperature: 13.8, humidity: 78,
        speed_kmh: 56, status: 'In Transit',
        event_type: 'exception',
        notes: 'CRITICAL: Cold-chain refrigeration power drop! Temp breached 8.0°C vaccine threshold.'
      });
      db.updateShipment('SHP-002', { temperature: 13.8 });
      broadcast({ event: 'shipment_update', data: db.getShipment('SHP-002') });
      broadcast({ event: 'new_event', data: ev });
      checkExceptions(ev, db.getShipment('SHP-002'), broadcast);
      addCheckpoint('SHP-002', 'TEMPERATURE_EXCURSION', { temperature: 13.8, limit: 8.0, trigger: 'Manual Viva Demo' });
      broadcast({ event: 'ledger_update', data: { shipment_id: 'SHP-002', event_type: 'TEMPERATURE_EXCURSION' } });
      return res.json({ success: true, scenario, message: 'Cold-chain thermal spike injected. Checkpoint mined.' });
    }
  } else if (scenario === 'highway_stoppage') {
    const s = db.getShipment('SHP-005');
    if (s) {
      const ev = db.insertEvent({
        shipment_id: 'SHP-005',
        lat: s.lat, lng: s.lng,
        temperature: s.temperature, humidity: s.humidity,
        speed_kmh: 0, status: 'Delayed',
        event_type: 'stoppage',
        notes: 'Unplanned vehicle breakdown on NH corridor: 0 km/h traffic halt.'
      });
      db.updateShipment('SHP-005', { status: 'Delayed', speed_kmh: 0 });
      broadcast({ event: 'shipment_update', data: db.getShipment('SHP-005') });
      broadcast({ event: 'new_event', data: ev });
      checkExceptions(ev, db.getShipment('SHP-005'), broadcast);
      return res.json({ success: true, scenario, message: 'Highway stoppage triggered. ML delay model updated.' });
    }
  } else if (scenario === 'checkpoint') {
    const b = addCheckpoint('SHP-001', 'WAYPOINT_CHECKPOINT', { notes: 'Passed major highway toll interchange on NH-44' });
    broadcast({ event: 'ledger_update', data: { shipment_id: 'SHP-001', event_type: 'WAYPOINT_CHECKPOINT' } });
    return res.json({ success: true, block: b, message: 'Manual waypoint checkpoint mined.' });
  }
  res.status(400).json({ error: 'Unknown scenario' });
});

// ── Fallback Route ────────────────────────────────────────────────────────────
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

// ── Stale tracking checker (every 5 min) ─────────────────────────────────────
setInterval(() => {
  checkStaleShipments(broadcast);
}, 5 * 60 * 1000);

// ── KPI broadcast (every 10s to keep dashboard live) ─────────────────────────
setInterval(() => {
  const kpis = db.kpis();
  broadcast({ event: 'kpi_update', data: kpis });
}, 10000);

// ── Start ─────────────────────────────────────────────────────────────────────
const PORT = process.env.PORT || 4001;
server.listen(PORT, () => {
  console.log(`\n🚀 Supply Chain Visibility Platform`);
  console.log(`   Server:    http://localhost:${PORT}`);
  console.log(`   WebSocket: ws://localhost:${PORT}`);
  console.log(`\n   ▶ Run the simulator: npm run simulate\n`);
});

module.exports = { app, server, broadcast };

/**
 * Pure JSON file-based data store.
 * Replaces SQLite to avoid native compilation issues.
 * Data is persisted in data/db.json on every write.
 */
const fs   = require('fs');
const path = require('path');

const DATA_DIR  = path.join(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'db.json');

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// ── In-memory store ───────────────────────────────────────────────────────────
let store = {
  shipments: [],
  events:    [],
  alerts:    [],
  ledger:    [],
  _nextEventId: 1,
  _nextAlertId: 1,
  _nextLedgerId: 1,
};

// ── Load from disk ────────────────────────────────────────────────────────────
function load() {
  if (fs.existsSync(DATA_FILE)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
      if (parsed && Array.isArray(parsed.shipments) && parsed.shipments.length > 0) {
        store = parsed;
        if (!store.events) store.events = [];
        if (!store.alerts) store.alerts = [];
        if (!store.ledger) store.ledger = [];
        if (!store._nextEventId) store._nextEventId = store.events.length + 1;
        if (!store._nextAlertId) store._nextAlertId = store.alerts.length + 1;
        if (!store._nextLedgerId) store._nextLedgerId = store.ledger.length + 1;
      }
    } catch(e) {
      console.warn('[DB] Could not parse db.json, starting fresh.');
    }
  }
}

// ── Save to disk (debounced) ──────────────────────────────────────────────────
let saveTimer = null;
function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      fs.writeFileSync(DATA_FILE, JSON.stringify(store, null, 2));
    } catch (err) {
      console.error('[DB] Error writing db.json:', err.message);
    }
  }, 300);
}

// ── Seed initial data if empty ────────────────────────────────────────────────
function seed() {
  if (store.shipments.length > 0) return;
  const now = new Date();
  const addDays = (d) => new Date(now.getTime() + d * 86400000).toISOString();

  store.shipments = [
    {
      id: 'SHP-001',
      name: 'Electronics – Chennai to Delhi',
      origin: 'Chennai, TN',
      destination: 'New Delhi, DL',
      carrier: 'Blue Dart Express',
      status: 'In Transit',
      eta: addDays(2),
      created_at: now.toISOString(),
      lat: 14.92,
      lng: 79.84,
      temperature: 28.0,
      humidity: 60,
      progress: 35,
      shipper: 'Samsung India Pvt. Ltd.',
      consignee: 'Croma Retail Ltd.',
      owner_contact: '+91-44-2810-9900',
      consignee_contact: '+91-11-4567-8900',
      cargo_type: 'Consumer Electronics (Smartphones & Accessories)',
      weight_kg: 2400,
      value_inr: 4800000,
      tracking_ref: 'BDEX-24-CHN-DEL-001',
    },
    {
      id: 'SHP-002',
      name: 'Pharma Cold Chain – Mumbai to Kolkata',
      origin: 'Mumbai, MH',
      destination: 'Kolkata, WB',
      carrier: 'TCI Cold Chain',
      status: 'In Transit',
      eta: addDays(1),
      created_at: now.toISOString(),
      lat: 21.44,
      lng: 73.01,
      temperature: 4.8,
      humidity: 72,
      progress: 28,
      shipper: 'Cipla Limited',
      consignee: 'Fortis Healthcare Ltd.',
      owner_contact: '+91-22-2482-6000',
      consignee_contact: '+91-33-4628-9000',
      cargo_type: 'Temperature-Sensitive Pharmaceuticals (Vaccines)',
      weight_kg: 320,
      value_inr: 9200000,
      tracking_ref: 'TCI-CC-MUM-KOL-002',
    },
    {
      id: 'SHP-003',
      name: 'Textile Export – Surat to JNPT Port',
      origin: 'Surat, GJ',
      destination: 'JNPT Port, MH',
      carrier: 'Maersk India',
      status: 'In Transit',
      eta: addDays(1),
      created_at: now.toISOString(),
      lat: 20.90,
      lng: 73.00,
      temperature: 31.0,
      humidity: 65,
      progress: 50,
      shipper: 'Arvind Mills Ltd.',
      consignee: 'Maersk Logistics India',
      owner_contact: '+91-261-248-1100',
      consignee_contact: '+91-22-6691-2000',
      cargo_type: 'Raw Cotton & Woven Fabrics',
      weight_kg: 18000,
      value_inr: 3400000,
      tracking_ref: 'MSK-IN-SRT-JNP-003',
    },
    {
      id: 'SHP-004',
      name: 'Auto Parts – Pune to Bengaluru',
      origin: 'Pune, MH',
      destination: 'Bengaluru, KA',
      carrier: 'V-Trans Logistics',
      status: 'In Transit',
      eta: addDays(2),
      created_at: now.toISOString(),
      lat: 16.85,
      lng: 74.58,
      temperature: 27.5,
      humidity: 55,
      progress: 42,
      shipper: 'Bharat Forge Ltd.',
      consignee: 'Bosch Automotive India',
      owner_contact: '+91-20-2670-2000',
      consignee_contact: '+91-80-6752-1111',
      cargo_type: 'Precision Automotive Components & Crankshafts',
      weight_kg: 4100,
      value_inr: 6200000,
      tracking_ref: 'VT-PUN-BLR-004',
    },
    {
      id: 'SHP-005',
      name: 'FMCG Consumer Goods – Ahmedabad to Guwahati',
      origin: 'Ahmedabad, GJ',
      destination: 'Guwahati, AS',
      carrier: 'Delhivery Surface',
      status: 'In Transit',
      eta: addDays(4),
      created_at: now.toISOString(),
      lat: 24.58,
      lng: 73.71,
      temperature: 29.0,
      humidity: 58,
      progress: 22,
      shipper: 'Adani Wilmar Ltd.',
      consignee: 'North-East Retail Distributors',
      owner_contact: '+91-79-2656-5555',
      consignee_contact: '+91-361-234-8800',
      cargo_type: 'Packaged Food & FMCG Essentials',
      weight_kg: 6200,
      value_inr: 2200000,
      tracking_ref: 'DEL-AMD-GAU-005',
    },
  ];
  save();
}

// ── Database Methods ──────────────────────────────────────────────────────────
const db = {
  // Shipments
  getShipments() {
    return store.shipments;
  },
  getShipment(id) {
    return store.shipments.find(s => s.id === id) || null;
  },
  updateShipment(id, patch) {
    const s = store.shipments.find(s => s.id === id);
    if (s) {
      Object.assign(s, patch);
      save();
    }
    return s;
  },

  // Events
  insertEvent(e) {
    e.id = store._nextEventId++;
    e.timestamp = e.timestamp || new Date().toISOString();
    store.events.push(e);
    save();
    return e;
  },
  getEvents(shipmentId, limit = 50) {
    return store.events
      .filter(e => e.shipment_id === shipmentId)
      .sort((a, b) => b.timestamp.localeCompare(a.timestamp))
      .slice(0, limit);
  },
  getEventsSince(shipmentId, since) {
    return store.events.filter(e => e.shipment_id === shipmentId && e.timestamp >= since);
  },
  countEvents() {
    return store.events.length;
  },

  // Alerts
  insertAlert(a) {
    a.id          = store._nextAlertId++;
    a.created_at  = new Date().toISOString();
    a.resolved    = 0;
    a.resolved_at = null;
    store.alerts.push(a);
    save();
    return a;
  },
  getAlerts(resolved = 0, limit = 100) {
    const shipMap = Object.fromEntries(store.shipments.map(s => [s.id, s]));
    return store.alerts
      .filter(a => a.resolved === resolved)
      .sort((a, b) => b.created_at.localeCompare(a.created_at))
      .slice(0, limit)
      .map(a => ({
        ...a,
        shipment_name: shipMap[a.shipment_id]?.name || '',
        carrier: shipMap[a.shipment_id]?.carrier || ''
      }));
  },
  getAlertsByShipment(shipmentId) {
    return store.alerts
      .filter(a => a.shipment_id === shipmentId)
      .sort((a, b) => b.created_at.localeCompare(a.created_at));
  },
  resolveAlert(id) {
    const alertId = parseInt(id);
    const a = store.alerts.find(a => a.id === alertId && a.resolved === 0);
    if (!a) return false;
    a.resolved = 1;
    a.resolved_at = new Date().toISOString();
    save();
    return true;
  },
  countActiveAlerts() {
    return store.alerts.filter(a => a.resolved === 0).length;
  },
  alertSummary() {
    const active = store.alerts.filter(a => a.resolved === 0);
    const bySev  = {};
    for (const a of active) bySev[a.severity] = (bySev[a.severity] || 0) + 1;
    return {
      total: active.length,
      bySeverity: Object.entries(bySev).map(([severity, count]) => ({ severity, count }))
    };
  },
  hasActiveAlert(shipmentId, type) {
    return store.alerts.some(a => a.shipment_id === shipmentId && a.type === type && a.resolved === 0);
  },
  clearAlert(shipmentId, type) {
    const a = store.alerts.find(a => a.shipment_id === shipmentId && a.type === type && a.resolved === 0);
    if (a) {
      a.resolved = 1;
      a.resolved_at = new Date().toISOString();
      save();
    }
  },

  // Ledger
  insertLedgerBlock(b) {
    b.id = store._nextLedgerId++;
    b.timestamp = new Date().toISOString();
    store.ledger.push(b);
    save();
    return b;
  },
  getLatestBlock() {
    return store.ledger.length > 0 ? store.ledger[store.ledger.length - 1] : null;
  },
  getLedger(limit = 20) {
    return [...store.ledger].reverse().slice(0, limit);
  },
  getAllLedger() {
    return store.ledger;
  },
  countLedger() {
    return store.ledger.length;
  },

  // Analytics & KPIs
  kpis() {
    const s = store.shipments;
    const total      = s.length;
    const inTransit  = s.filter(x => x.status === 'In Transit').length;
    const delayed    = s.filter(x => x.status === 'Delayed').length;
    const delivered  = s.filter(x => x.status === 'Delivered').length;
    const exceptions = s.filter(x => x.status === 'Exception').length;
    const activeAlerts = this.countActiveAlerts();
    const critAlerts   = store.alerts.filter(a => a.resolved === 0 && a.severity === 'critical').length;
    const totalEvents  = store.events.length;
    const onTimeRate   = total > 0 ? Math.round(((total - delayed - exceptions) / total) * 100) : 100;
    const ledgerCount  = this.countLedger();
    return { total, inTransit, delayed, delivered, exceptions, activeAlerts, critAlerts, totalEvents, onTimeRate, ledgerCount };
  },
  carrierPerf() {
    const map = {};
    for (const s of store.shipments) {
      if (!map[s.carrier]) map[s.carrier] = { carrier: s.carrier, total_shipments: 0, delayed: 0, delivered: 0, temps: [] };
      map[s.carrier].total_shipments++;
      if (s.status === 'Delayed')   map[s.carrier].delayed++;
      if (s.status === 'Delivered') map[s.carrier].delivered++;
      map[s.carrier].temps.push(s.temperature || 22);
    }
    return Object.values(map).map(c => ({
      ...c,
      avg_temperature: (c.temps.reduce((a, b) => a + b, 0) / c.temps.length).toFixed(1)
    }));
  },
  tempHistory(shipmentId, limit = 100) {
    return store.events
      .filter(e => e.shipment_id === shipmentId)
      .sort((a, b) => a.timestamp.localeCompare(b.timestamp))
      .slice(-limit)
      .map(e => ({ timestamp: e.timestamp, temperature: e.temperature, humidity: e.humidity }));
  },
  eventFrequency() {
    const cutoff = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
    const buckets = {};
    for (const e of store.events) {
      if (e.timestamp < cutoff) continue;
      const hour = e.timestamp.slice(0, 13) + ':00';
      buckets[hour] = (buckets[hour] || 0) + 1;
    }
    return Object.entries(buckets).sort((a, b) => a[0].localeCompare(b[0])).map(([hour, count]) => ({ hour, count }));
  },
  alertTrend() {
    const cutoff = new Date(Date.now() - 7 * 24 * 3600 * 1000).toISOString();
    const buckets = {};
    for (const a of store.alerts) {
      if (a.created_at < cutoff) continue;
      const day = a.created_at.slice(0, 10);
      const key = `${day}|${a.severity}`;
      buckets[key] = (buckets[key] || 0) + 1;
    }
    return Object.entries(buckets).sort((a, b) => a[0].localeCompare(b[0])).map(([k, count]) => {
      const [day, severity] = k.split('|');
      return { day, severity, count };
    });
  },
};

load();
seed();

module.exports = db;
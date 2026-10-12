const db = require('./db');

const CARRIER_DELAY_RATE = {
  'DHL Express': 0.12, 'FedEx Pharma': 0.18, 'Maersk Line': 0.22,
  'MSC Shipping': 0.25, 'Air France Cargo': 0.15, 'default': 0.20,
};

function getSeasonMultiplier() {
  const m = new Date().getMonth();
  if ([10,11,0].includes(m)) return 1.4;
  if ([2,3].includes(m))     return 1.15;
  return 1.0;
}

function predictDelay(shipmentId) {
  const shipment = db.getShipment(shipmentId);
  if (!shipment) return null;
  const events = db.getEvents(shipmentId, 30);
  const factors = []; let score = 0;

  // Feature 1: Carrier reliability
  const rate = CARRIER_DELAY_RATE[shipment.carrier] || CARRIER_DELAY_RATE['default'];
  const c1 = rate * 100 * 0.25;
  score += c1;
  factors.push({ name: 'Carrier Reliability', contribution: Math.round(c1), detail: `${(rate*100).toFixed(0)}% historical delay rate` });

  // Feature 2: Temperature stress
  if (events.length > 0) {
    const avg = events.reduce((s,e) => s + (e.temperature||22), 0) / events.length;
    const dev = Math.abs(avg - 22);
    if (dev > 5) {
      const c2 = Math.min(dev*3,40) * 0.20;
      score += c2;
      factors.push({ name: 'Temperature Stress', contribution: Math.round(c2), detail: `Avg ${avg.toFixed(1)}°C (${dev.toFixed(1)}° from optimal)` });
    }
  }

  // Feature 3: Schedule adherence
  const etaDate   = new Date(shipment.eta);
  const createdDate = new Date(shipment.created_at);
  const totalDur  = etaDate - createdDate;
  const elapsed   = Date.now() - createdDate;
  const timePct   = Math.min(elapsed / (totalDur||1), 1);
  const locPct    = (shipment.progress || 0) / 100;
  const gap = timePct - locPct;
  if (gap > 0.1) {
    const c3 = Math.min(gap*100,50)*0.30;
    score += c3;
    factors.push({ name: 'Schedule Adherence', contribution: Math.round(c3), detail: `${(gap*100).toFixed(0)}% behind schedule` });
  }

  // Feature 4: Stoppages
  const stops = events.filter(e => (e.speed_kmh||0) < 2 && e.status !== 'Checkpoint').length;
  if (stops > 3) {
    const c4 = Math.min(stops*5,30)*0.15;
    score += c4;
    factors.push({ name: 'Unplanned Stoppages', contribution: Math.round(c4), detail: `${stops} low-speed events` });
  }

  // Feature 5: Peak season
  const sm = getSeasonMultiplier();
  if (sm > 1.0) {
    const c5 = (sm-1.0)*60*0.10;
    score += c5;
    factors.push({ name: 'Peak Season', contribution: Math.round(c5), detail: `×${sm.toFixed(2)} multiplier` });
  }

  score = Math.min(Math.round(score), 100);
  const label = score < 20 ? 'LOW' : score < 45 ? 'MEDIUM' : score < 70 ? 'HIGH' : 'CRITICAL';
  return { shipmentId, riskScore: score, label, factors };
}

function predictAllShipments() {
  return db.getShipments()
    .filter(s => s.status !== 'Delivered')
    .map(s => predictDelay(s.id))
    .filter(Boolean);
}

module.exports = { predictDelay, predictAllShipments };

const db = require('./db');
const { addCheckpoint } = require('./blockchain-ledger');

const THRESHOLDS = {
  TEMPERATURE_HIGH: 30.0, TEMPERATURE_LOW: 2.0,
  PHARMA_TEMP_HIGH: 8.0,  PHARMA_TEMP_LOW: 2.0,
  NO_UPDATE_MINUTES: 15,  DELAY_HOURS: 2, SPEED_MAX_KMH: 1200,
};
const PHARMA_CARRIERS = ['FedEx Pharma', 'UPS Cold Chain'];

function raiseAlert(shipmentId, type, severity, message, broadcast) {
  if (db.hasActiveAlert(shipmentId, type)) return null;
  const a = db.insertAlert({ shipment_id: shipmentId, type, severity, message });
  if (broadcast) broadcast({ event: 'alert', data: a });
  return a;
}

function checkExceptions(event, shipment, broadcast) {
  const alerts = [];
  const isPharma = PHARMA_CARRIERS.includes(shipment.carrier);
  const tempHigh = isPharma ? THRESHOLDS.PHARMA_TEMP_HIGH : THRESHOLDS.TEMPERATURE_HIGH;
  const tempLow  = isPharma ? THRESHOLDS.PHARMA_TEMP_LOW  : THRESHOLDS.TEMPERATURE_LOW;

  if (event.temperature > tempHigh) {
    const a = raiseAlert(shipment.id, 'TEMP_HIGH', isPharma ? 'critical' : 'high',
      `Temperature ${event.temperature.toFixed(1)}°C exceeds limit ${tempHigh}°C — ${shipment.name}`, broadcast);
    if (a) { alerts.push(a); addCheckpoint(shipment.id, 'TEMPERATURE_EXCURSION', { temperature: event.temperature, limit: tempHigh }); }
  } else if (event.temperature < tempLow) {
    const a = raiseAlert(shipment.id, 'TEMP_LOW', 'high',
      `Temperature ${event.temperature.toFixed(1)}°C below minimum ${tempLow}°C — ${shipment.name}`, broadcast);
    if (a) alerts.push(a);
  } else {
    db.clearAlert(shipment.id, 'TEMP_HIGH');
    db.clearAlert(shipment.id, 'TEMP_LOW');
  }

  const hoursOverdue = (Date.now() - new Date(shipment.eta).getTime()) / 3600000;
  if (hoursOverdue > THRESHOLDS.DELAY_HOURS && shipment.status !== 'Delivered') {
    const a = raiseAlert(shipment.id, 'ETA_BREACH', 'high',
      `${shipment.id} is ${hoursOverdue.toFixed(1)}h past ETA. Status: ${shipment.status}`, broadcast);
    if (a) {
      alerts.push(a);
      db.updateShipment(shipment.id, { status: 'Delayed' });
      addCheckpoint(shipment.id, 'ETA_BREACH', { hoursOverdue });
    }
  }

  if (event.speed_kmh > THRESHOLDS.SPEED_MAX_KMH) {
    const a = raiseAlert(shipment.id, 'SPEED_ANOMALY', 'medium',
      `Implausible speed ${event.speed_kmh} km/h — possible GPS error for ${shipment.id}`, broadcast);
    if (a) alerts.push(a);
  }
  return alerts;
}

function checkStaleShipments(broadcast) {
  const shipments = db.getShipments().filter(s => s.status !== 'Delivered');
  const cutoff = new Date(Date.now() - THRESHOLDS.NO_UPDATE_MINUTES * 60000).toISOString();
  for (const s of shipments) {
    const evts = db.getEventsSince(s.id, cutoff);
    if (!evts.length) {
      raiseAlert(s.id, 'STALE_TRACKING', 'medium',
        `No update for ${s.id} (${s.name}) in ${THRESHOLDS.NO_UPDATE_MINUTES}+ minutes`, broadcast);
    } else {
      db.clearAlert(s.id, 'STALE_TRACKING');
    }
  }
}

module.exports = { checkExceptions, checkStaleShipments, THRESHOLDS };

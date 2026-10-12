const express = require('express');
const router  = express.Router();
const db      = require('../db');
const { checkExceptions }  = require('../exception-engine');
const { addCheckpoint }    = require('../blockchain-ledger');

let _broadcast = null;
function setBroadcast(fn) { _broadcast = fn; }

router.post('/', (req, res) => {
  const { shipment_id, lat, lng, temperature, humidity, speed_kmh, status, event_type, notes, progress } = req.body;
  if (!shipment_id || lat === undefined || lng === undefined)
    return res.status(400).json({ error: 'shipment_id, lat, lng required' });

  const shipment = db.getShipment(shipment_id);
  if (!shipment) return res.status(404).json({ error: 'Shipment not found' });

  const ev = db.insertEvent({
    shipment_id, lat, lng,
    temperature: temperature ?? 22, humidity: humidity ?? 55,
    speed_kmh: speed_kmh ?? 0, status: status ?? 'Moving',
    event_type: event_type ?? 'location_update', notes: notes ?? '',
  });

  // Update shipment position
  db.updateShipment(shipment_id, {
    lat, lng,
    temperature: temperature ?? shipment.temperature,
    humidity:    humidity    ?? shipment.humidity,
    progress:    progress    !== undefined ? progress : shipment.progress,
  });

  if (_broadcast) {
    _broadcast({ event: 'shipment_update', data: db.getShipment(shipment_id) });
    _broadcast({ event: 'new_event', data: ev });
  }

  const fresh = db.getShipment(shipment_id);
  checkExceptions(ev, fresh, _broadcast);

  const criticalTypes = ['checkpoint','delivery','exception','pickup'];
  if (criticalTypes.includes((event_type||'').toLowerCase())) {
    addCheckpoint(shipment_id, (event_type||'').toUpperCase(), { lat, lng, status });
    if (_broadcast) _broadcast({ event: 'ledger_update', data: { shipment_id, event_type } });
  }

  res.status(201).json({ message: 'Event recorded', id: ev.id });
});

router.get('/:shipmentId', (req, res) => {
  res.json(db.getEvents(req.params.shipmentId, parseInt(req.query.limit) || 50));
});

module.exports = { router, setBroadcast };

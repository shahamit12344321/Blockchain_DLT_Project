const crypto = require('crypto');
const db = require('./db');

let originalTamperedBlock = null;

function computeHash(prevHash, data, nonce) {
  return crypto.createHash('sha256').update(prevHash + data + String(nonce)).digest('hex');
}

function mineBlock(prevHash, data) {
  let nonce = 0, hash;
  do {
    hash = computeHash(prevHash, data, nonce);
    nonce++;
  } while (!hash.startsWith('00'));
  return { hash, nonce: nonce - 1 };
}

function initGenesis() {
  if (db.countLedger() > 0) return;
  const zeroHash = '0'.repeat(64);
  const data = JSON.stringify({ type: 'GENESIS', message: 'Supply Chain Ledger Initialized' });
  const { hash, nonce } = mineBlock(zeroHash, data);
  db.insertLedgerBlock({ hash, prev_hash: zeroHash, data, nonce });
  console.log('[Ledger] Genesis block:', hash.slice(0, 16) + '...');
}

function addCheckpoint(shipmentId, eventType, payload) {
  const latest = db.getLatestBlock();
  const data   = JSON.stringify({ shipment_id: shipmentId, event_type: eventType, timestamp: new Date().toISOString(), payload });
  const { hash, nonce } = mineBlock(latest.hash, data);
  return db.insertLedgerBlock({ hash, prev_hash: latest.hash, data, nonce });
}

function getChain(limit = 20) {
  return db.getLedger(limit);
}

function verifyChain() {
  const blocks = db.getAllLedger();
  for (let i = 1; i < blocks.length; i++) {
    const b = blocks[i];
    if (computeHash(b.prev_hash, b.data, b.nonce) !== b.hash) return { valid: false, failedAt: b.id };
    if (b.prev_hash !== blocks[i - 1].hash) return { valid: false, failedAt: b.id };
  }
  return { valid: true, length: blocks.length };
}

function tamperBlock(blockId, forgedData) {
  const blocks = db.getAllLedger();
  // If no blockId provided, tamper with the latest non-genesis block, or block 2
  const targetId = blockId ? parseInt(blockId) : (blocks.length > 1 ? blocks[1].id : 1);
  const target = blocks.find(b => b.id === targetId);
  if (!target) return null;
  if (!originalTamperedBlock) {
    originalTamperedBlock = { id: target.id, data: target.data };
  }
  target.data = forgedData || JSON.stringify({
    shipment_id: 'SHP-002',
    event_type: 'TAMPERED_RECORD',
    payload: { temperature: 4.0, note: 'ATTACKER_ALTERED_PAYLOAD_UNAUTHORIZED' }
  });
  return { tamperedId: target.id, data: target.data };
}

function restoreTamperedBlock() {
  if (!originalTamperedBlock) return false;
  const blocks = db.getAllLedger();
  const target = blocks.find(b => b.id === originalTamperedBlock.id);
  if (target) {
    target.data = originalTamperedBlock.data;
    originalTamperedBlock = null;
    return true;
  }
  return false;
}

initGenesis();
module.exports = { addCheckpoint, getChain, verifyChain, tamperBlock, restoreTamperedBlock };

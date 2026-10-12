#!/usr/bin/env bash

# ==============================================================================
# ChainVision Pro — Review 2 One-Click Demo Launcher
# Vellore Institute of Technology (VIT) • Blockchain & DLT Project Review 2
# ==============================================================================

PORT=4001

echo ""
echo "=================================================================="
echo "🌐 ChainVision Pro — Real-Time Supply Chain Visibility Platform"
echo "   Review 2 Demonstration Launcher"
echo "=================================================================="
echo ""

# 1. Start backend server in background
echo "▶ [1/3] Starting Backend Server & Blockchain Ledger on port $PORT..."
PORT=$PORT node server/index.js &
SERVER_PID=$!

# Ensure server and simulator terminate cleanly when user presses Ctrl+C
cleanup() {
  echo ""
  echo "⏹ Shutting down server (PID $SERVER_PID)..."
  kill "$SERVER_PID" 2>/dev/null
  echo "✓ ChainVision Pro stopped cleanly."
  exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 2. Wait for server socket to initialize
sleep 1.5

# 3. Automatically launch dashboard in default browser
echo "▶ [2/3] Opening Live Operations Dashboard in your browser..."
open "http://localhost:$PORT" 2>/dev/null || true

# 4. Run IoT Telemetry Simulator in foreground
echo "▶ [3/3] Starting IoT/GPS Route Simulator (5 shipments across Indian corridors)..."
echo "------------------------------------------------------------------"
echo "💡 TIP: Press Ctrl+C in this terminal whenever you want to stop the demo."
echo "------------------------------------------------------------------"
echo ""

PORT=$PORT node simulator/simulate.js

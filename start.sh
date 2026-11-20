#!/usr/bin/env bash
# Start all three components of the Customer Billing Review Agent solution.
# Usage: ./start.sh
# Prerequisite: copy agent/.env.example to agent/.env and fill in AI credentials.

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Starting Customer Billing Review Agent ==="

# Start Python agent
echo "[1/3] Starting Python agent on port 8000..."
cd "$ROOT_DIR/agent"
pip install -q -r requirements.txt
python server.py &
AGENT_PID=$!
echo "    Agent PID: $AGENT_PID"

# Wait for agent to be ready
sleep 2

# Start CAP backend
echo "[2/3] Starting CAP backend on port 4004..."
cd "$ROOT_DIR/backend"
AGENT_BASE_URL=http://localhost:8000 npm run dev &
CAP_PID=$!
echo "    CAP PID: $CAP_PID"

# Wait for CAP to be ready
sleep 3

# Start UI dev server
echo "[3/3] Starting UI on port 5173..."
cd "$ROOT_DIR/ui"
npm run dev &
UI_PID=$!
echo "    UI PID: $UI_PID"

echo ""
echo "=== All services started ==="
echo "   UI:      http://localhost:5173"
echo "   Backend: http://localhost:4004"
echo "   Agent:   http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services."

trap "kill $AGENT_PID $CAP_PID $UI_PID 2>/dev/null" EXIT
wait

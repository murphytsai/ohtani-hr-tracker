#!/bin/bash
# vibe-template-version: 1
set -eo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Smart Port Discovery — find an available port starting from 8000
find_available_port() {
  local PORT=$1
  while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
  done
  echo $PORT
}

# Register process group ID immediately — crash-safe cleanup anchor
OLD_PGID=$(cat .vibe.pgid 2>/dev/null || true)
echo $$ > .vibe.pgid
if [ -n "$OLD_PGID" ]; then
  kill -9 -- -$OLD_PGID 2>/dev/null && echo "🧹 Killed previous instance (PGID: $OLD_PGID)" || true
fi
rm -f .vibe_ports

PORT=$(find_available_port "${APP_PORT:-8000}")
echo "web:$PORT" > .vibe_ports
echo "⚾ Starting MLB Shohei Ohtani HR Tracker on port $PORT..."
echo "Local: http://localhost:$PORT"

# Run in foreground with exec so vibe-pm can manage the process lifecycle
exec uv run python -m http.server "$PORT"
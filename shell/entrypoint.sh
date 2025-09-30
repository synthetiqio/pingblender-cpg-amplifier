#!/bin/bash
. /venv/bin/activate
cd /app/signals
CMD="uvicorn synthetiq:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000}"
echo "SynthetIQ Signals Systems: OK"
exec $CMD
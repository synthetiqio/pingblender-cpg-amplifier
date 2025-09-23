#!/bin/bash
. /venv/bin/activate
cd /app/signals

echo "${APP_HOST} is where this is headed"

CMD="uvicorn synthetiq:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-1010}"
if ["${APP_RELOAD}" = true]; then
    CMD="$CMD --reload"
fi

echo "SynthetIQ Signals Systems: OK"
exec $CMD

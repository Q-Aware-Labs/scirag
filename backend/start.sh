#!/bin/bash
# Railway start script - ensures PORT is properly set

# Set default port if PORT is not set or is literally "$PORT"
if [ -z "$PORT" ] || [ "$PORT" = "\$PORT" ]; then
    export PORT=8000
fi

echo "Starting uvicorn on port $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
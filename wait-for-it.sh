#!/usr/bin/env bash
# wait-for-it.sh - wait until a service is ready
# Usage: ./wait-for-it.sh host:port -- command args

set -e

HOSTPORT="$1"
shift
COMMAND="$@"

HOST=$(echo "$HOSTPORT" | cut -d: -f1)
PORT=$(echo "$HOSTPORT" | cut -d: -f2)

echo "Waiting for $HOST:$PORT..."
until nc -z "$HOST" "$PORT"; do
  sleep 1
done

echo "$HOST:$PORT is available, running command..."
exec $COMMAND

#!/bin/bash

PROJECT_DIR=$(pwd)

# Start REST API
gnome-terminal -- bash -c "cd $PROJECT_DIR && source venv/bin/activate && python backend/rest_api/app.py & echo \$! > rest_api.pid; exec bash"

# Start GraphQL API
gnome-terminal -- bash -c "cd $PROJECT_DIR && source venv/bin/activate && python backend/graphql_api/app.py & echo \$! > graphql_api.pid; exec bash"

# Wait for REST API
echo "Waiting for REST API (port 5001)..."
while ! nc -z localhost 5001; do sleep 0.5; done
echo "REST API is up!"

# Wait for GraphQL API
echo "Waiting for GraphQL API (port 5002)..."
while ! nc -z localhost 5002; do sleep 0.5; done
echo "GraphQL API is up!"

# Export PIDs as env vars if needed
export REST_PID=$REST_PID
export GRAPHQL_PID=$GRAPHQL_PID

# Run comparison every 10 seconds in background
echo "Starting comparison loop..."
gnome-terminal -- bash -c "cd $PROJECT_DIR && source venv/bin/activate && while true; do python backend/observer/compare.py; sleep 10; done" &

# Start dashboard
echo "Starting dashboard..."
source venv/bin/activate && python dashboard.py


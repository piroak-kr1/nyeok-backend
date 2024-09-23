# Locally run the backend service

# 1. Run local database script in background
./scripts/local/database.sh &
DB_PID=$!  # Store the PID of the database process

# 2. wait for start local database to signal that it is ready
PIPE=/tmp/port-forward-pipe
if [[ ! -p $PIPE ]]; then
  mkfifo $PIPE
fi
read < $PIPE  # Wait for the signal

# 2. Run backend service
\cd "./backend-service"
# NOTE: Real environment does not change
\poetry run bash -c "export RUNTIME_TYPE=dev; cd backend_service && fastapi dev"

# 3. User finished fastapi process by pressing Ctrl+C at this terminal
# All processes in current process group is killed (including start_local_database)

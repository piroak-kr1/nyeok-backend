# Description: Start local database for development

# Start minikube if not running
this_script_dir=$(dirname "$0")
"$this_script_dir/start_minikube.sh"

# 1. Check if port-forward is already running
PID=$(lsof -i:5432 -t)
if [ -n "$PID" ]; then
  # Kill the process
  echo "Killing existing port-forward process with PID $PID"
  kill -9 $PID
fi

# 2. Start port-forward
#    NOTE: This is long running process
#    User should interrupt this script when done
\kubectl port-forward svc/postgres-svc 5432:5432 &
PID=$!  # Store the PID of port-forward process

# 3. Signal that port-forward is ready
# Create a named pipe for synchronization
PIPE=/tmp/port-forward-pipe
if [[ ! -p $PIPE ]]; then
  mkfifo $PIPE
fi
echo "ready" > $PIPE  # Send a signal through the named pipe

# 4. Wait for user to interrupt this script
wait $PID

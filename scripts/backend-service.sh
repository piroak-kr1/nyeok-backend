scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"
start_local_database="$scripts_dir/kubernetes/start_local_database.sh"

# Run script in background
"$start_local_database" > /dev/null 2>&1 &
"$runpoetry" backend-service/backend_service fastapi dev

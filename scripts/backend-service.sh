runpoetry="./scripts/runpoetry.sh"
start_local_database="./scripts/kubernetes/start_local_database.sh"

# Run script in background
"$start_local_database" > /dev/null 2>&1 &
"$runpoetry" backend-service/backend_service fastapi dev

scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"

"$runpoetry" backend-service/backend_service fastapi dev

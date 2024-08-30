runpoetry="./scripts/runpoetry.sh"
start_local_database="./scripts/kubernetes/start_local_database.sh"

# Run script in background
# TODO: need some time
"$start_local_database" > /dev/null 2>&1 &
"$runpoetry" database-setup/ python -m database_setup.main

scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"

"$runpoetry" database-setup/database_setup/ python -m database_setup.main

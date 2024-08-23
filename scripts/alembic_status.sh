scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"

echo "== Running Alembic History =="
"$runpoetry" database-setup/database_setup alembic history

echo ""
echo "== Running Alembic Current =="
"$runpoetry" database-setup/database_setup alembic current

echo ""
echo "== Running Alembic Check =="
"$runpoetry" database-setup/database_setup alembic check

scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"

echo "== Running Alembic History =="
"$runpoetry" database-setup/database_setup alembic history

echo ""
echo "== Running Alembic Current =="
"$runpoetry" database-setup/database_setup alembic current 2>/dev/null

echo ""
echo "== Running Alembic Check =="
"$runpoetry" database-setup/database_setup alembic check 2>/dev/null

# NOTE: Ways to delete revision
# delete a file in alembic/versions
# DELETE FROM alembic_version where version_num='61b069ea7b7c'; (If it is committed to DB)

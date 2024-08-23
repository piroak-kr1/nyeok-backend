from database_core import db
from database_core.tables import Place

db.setup(
    username="superuser",
    password="wrongpassword",
    hostname="localhost",
    port=5432,
    databasename="database",
)
session = db.get_session_with()

with session:
    print(session.query(Place).all())

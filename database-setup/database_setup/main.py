from database_core import db
from database_core.tables import Place

from .tourapi import AreaBasedListAPI
from .tourapi.AreaCode import AreaCode

if __name__ == "__main__":
    db.setup(
        username="superuser",
        password="wrongpassword",
        hostname="localhost",
        port=5432,
        databasename="database",
    )

    params = AreaBasedListAPI.Params(
        numOfRows=10,
        pageNo=1,
        areaCode=int(AreaCode.서울),
        sigunguCode=AreaCode.서울.마포구,
        contentTypeId=None,
        arrange="O",
        listYN=None,
        cat1=None,
        cat2=None,
        cat3=None,
    )
    for item in AreaBasedListAPI.AreaBasedListAPI.get_items_all(params):
        print(f"{item.title=}")

    with db.get_session_with() as session:
        print(session.query(Place).all())

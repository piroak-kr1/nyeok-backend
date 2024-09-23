from nyeok_database_core import db
from nyeok_database_core.tables import Place

from .tourapi import AreaBasedListAPI
from .tourapi.AreaCode import AreaCode


def api_to_db_place(place: AreaBasedListAPI.Item) -> Place:
    return Place(
        contentid=place.contentid,
        title=place.title,
        coordinate=f"POINT({place.mapx} {place.mapy})",  # Well-Known Text
        firstimage2=place.firstimage2,
    )


if __name__ == "__main__":
    db.setup(
        username="superuser",
        password="wrongpassword",
        hostname="localhost",
        port=5432,
        databasename="database",
    )

    # Fetch data from API
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
    placeList: list[AreaBasedListAPI.Item] = (
        AreaBasedListAPI.AreaBasedListAPI.get_items_all(params)
    )

    dbPlaceList: list[Place] = list(map(api_to_db_place, placeList))
    print(f"All places: {len(dbPlaceList)=}")
    dbPlaceList = list(filter(lambda place: place.firstimage2 != "", dbPlaceList))
    print(f"Only places with image: {len(dbPlaceList)=}")
    # Insert to DB
    with db.get_session_with() as session:
        session.query(Place).delete()  # Delete all rows
        session.add_all(dbPlaceList)
        session.commit()

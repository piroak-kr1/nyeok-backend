from pydantic import BaseModel, HttpUrl
from pydantic_core import Url
from pydantic_extra_types.coordinate import Coordinate, Longitude, Latitude

from nyeok_database_core import tables


class Place(BaseModel):
    contentid: int
    title: str
    coordinate: Coordinate
    firstimage2: HttpUrl

    class Config:
        from_attributes = True  # SQLALchemy model to Pydantic model

    @staticmethod
    def from_sqlalchemy_model(dbPlace: tables.Place, longitude: float, latitude: float):
        return Place(
            contentid=dbPlace.contentid,
            title=dbPlace.title,
            coordinate=Coordinate(
                longitude=Longitude(longitude), latitude=Latitude(latitude)
            ),
            firstimage2=Url(dbPlace.firstimage2),
        )

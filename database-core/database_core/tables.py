from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from geoalchemy2 import Geometry


class TableBase(DeclarativeBase):
    pass


class Place(TableBase):
    __tablename__ = "place"
    contentid: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    coordinate: Mapped[Geometry] = mapped_column(Geometry("POINT"))
    firstimage2: Mapped[str]  # 썸네일 이미지

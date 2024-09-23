from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from geoalchemy2 import Geography


class TableBase(DeclarativeBase):
    pass


class Place(TableBase):
    __tablename__ = "place"
    contentid: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    coordinate: Mapped[Geography] = mapped_column(Geography("POINT", srid=4326))
    firstimage2: Mapped[str]  # 썸네일 이미지

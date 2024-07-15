from database.records import UserRecord
from sqlalchemy.orm import Session


def create(db: Session, user: UserRecord) -> UserRecord:
    db.add(user)
    db.commit()

    return user


def read_all(db: Session) -> list[UserRecord]:
    return db.query(UserRecord).all()


def read_by_username(db: Session, username: str) -> UserRecord | None:
    return db.query(UserRecord).filter(UserRecord.username == username).first()

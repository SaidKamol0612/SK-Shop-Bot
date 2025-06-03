from sqlalchemy import (
    BigInteger,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class User(Base):
    tg_id = mapped_column(BigInteger)
    name: Mapped[str]
    phone_num: Mapped[str]
    username: Mapped[str] = mapped_column(String, nullable=True)
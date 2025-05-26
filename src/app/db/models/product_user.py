from sqlalchemy import ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


from .base import Base
from .user import User

class Favorite(Base):
    user_id = mapped_column(ForeignKey(User.id))
    product_id: Mapped[int]
    
class Basket(Base):
    user_id = mapped_column(ForeignKey(User.id))
    is_ordered: Mapped[bool]
    
class ProductBasket(Base):
    basket_id = mapped_column(ForeignKey(Basket.id))
    product_id: Mapped[int]
    product_count: Mapped[int]
    
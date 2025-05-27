__all__ = (
    "main_router",
)

from .start_handler import router as main_router
from .main_handler import router as second
from .user_act_handler import router as third
from .catalog_handler import router as forth
from .favorite_handler import router as fifth
from .cart_handler import router as sixth
from .order_handler import router as seventh

main_router.include_router(second)
main_router.include_router(third)
main_router.include_router(forth)
main_router.include_router(fifth)
main_router.include_router(sixth)
main_router.include_router(seventh)
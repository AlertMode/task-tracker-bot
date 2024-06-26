__all__ = ('router',)

from aiogram import Router

from handlers.start_handler import router as start_router
from handlers.task_creation_handler import router as task_creation_router
from handlers.task_alteration_handler import router as task_alteration_router


router = Router(name=__name__)


router.include_routers(
    start_router,
    task_creation_router,
    task_alteration_router
)
__all__ = ('router',)

from aiogram import Router

from modules.start.start_handler import router as start_router
from modules.add.task_creation_handler import router as task_creation_router
from modules.list.task_list_handler import router as task_list_router


router = Router(name=__name__)


router.include_routers(
    start_router,
    task_creation_router,
    task_list_router
)
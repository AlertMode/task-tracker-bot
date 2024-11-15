__all__ = ('router',)

from aiogram import Router

from modules.start.start_handler import router as start_router
from modules.add.task_creation_handler import router as task_creation_router
from modules.alter.task_alteration_handler import router as task_alteration_router
from modules.list.task_list_handler import router as task_list_router
from modules.set.description_handler import router as description_handler_router
from modules.set.calendar_handler import router as calendar_handler_router
from modules.set.time_picker_handler import router as time_picker_router
from modules.set.time_zone_selector_handler import router as time_zone_selector_router

router = Router(name=__name__)


router.include_routers(
    start_router,
    task_creation_router,
    task_alteration_router,
    task_list_router,
    description_handler_router,
    calendar_handler_router,
    time_zone_selector_router,
    time_picker_router
)
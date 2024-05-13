__all__ = ('router', )

from aiogram import Router

from handlers.start.start import start_router
from handlers.create_task.create_task import create_task_router
from handlers.show_tasks.show_tasks import show_tasks_router 


router = Router()


router.include_routers(
    start_router,
    create_task_router,
    show_tasks_router
)
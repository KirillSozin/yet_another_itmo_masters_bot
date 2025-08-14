from . import common
from . import qa_handler

# Экспортируем роутеры для удобной регистрации в главном файле бота
routers = (
    common.router,
    qa_handler.router,
)

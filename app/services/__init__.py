from .yandex_assistant_service import YandexAssistantService  

# Это позволяет импортировать QAService напрямую из пакета services,
# например: from app.services import QAService
# вместо: from app.services.qa_service import QAService
__all__ = [
    "YandexAssistantService",
]

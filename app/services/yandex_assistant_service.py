# app/services/yandex_assistant_service.py
import json
from yandex_cloud_ml_sdk import YCloudML
from app.config import Settings

RAG_CONFIG_PATH = "data/rag_config.json"

class YandexAssistantService:
    def __init__(self, config: Settings):
        print("Инициализация сервиса ассистента Yandex...")
        self.sdk = YCloudML(folder_id=config.yandex_folder_id, auth=config.yandex_cloud_api_key)
        
        # Загружаем ID ассистента, созданного на предыдущем шаге
        with open(RAG_CONFIG_PATH, "r") as f:
            rag_config = json.load(f)
            assistant_id = rag_config.get("assistant_id")

        if not assistant_id:
            raise ValueError("ID ассистента не найден в rag_config.json. Запустите scripts/create_rag_assets.py")

        self.assistant = self.sdk.assistants.get(assistant_id)
        self.threads = {}  # In-memory хранилище для потоков диалога {chat_id: thread_object}
        print(f"Сервис готов. Работаем с ассистентом ID: {self.assistant.id}")

    def _get_or_create_thread(self, chat_id: int):
        """Получает или создает новый поток диалога для пользователя."""
        if chat_id in self.threads:
            return self.threads[chat_id]
        
        print(f"Создание нового потока для chat_id: {chat_id}")
        thread = self.sdk.threads.create()
        self.threads[chat_id] = thread
        return thread

    def ask(self, question: str, chat_id: int) -> str:
        """Задает вопрос ассистенту в рамках диалога с конкретным пользователем."""
        thread = self._get_or_create_thread(chat_id)
        
        try:
            # Отправляем сообщение в поток и запускаем ассистента
            thread.write(question)
            run = self.assistant.run(thread)
            
            # Ждем завершения работы ассистента
            result = run.wait()
            
            # Возвращаем текстовый ответ
            return result.text
        except Exception as e:
            print(f"Ошибка при общении с Assistant API: {e}")
            return "К сожалению, произошла ошибка при обработке вашего вопроса. Попробуйте еще раз позже."

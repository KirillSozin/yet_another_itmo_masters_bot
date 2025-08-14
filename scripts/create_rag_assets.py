import os
import json
from glob import glob
from yandex_cloud_ml_sdk import YCloudML
from app.config import load_config
from scripts.update_sources import fetch_and_parse

RAG_CONFIG_PATH = "data/rag_config.json"
SOURCE_DIR = "data/source_texts"

def main():
    print("1. Загрузка конфигурации...")
    config = load_config()

    print("2. Инициализация Yandex Cloud ML SDK...")
    sdk = YCloudML(folder_id=config.yandex_folder_id, auth=config.yandex_cloud_api_key)

    print("3. Обновление исходных текстовых файлов...")
    fetch_and_parse()

    print("4. Загрузка файлов в Yandex Cloud...")
    source_files = glob(os.path.join(SOURCE_DIR, "*.txt"))
    uploaded_files = [
        sdk.files.upload(file, ttl_days=5, expiration_policy="static")
        for file in source_files
    ]
    uploaded_file_ids = [file.id for file in uploaded_files]
    print(f"Загружено {len(uploaded_file_ids)} файлов.")

    print("5. Создание поискового индекса (SearchIndex)... Это может занять несколько минут.")
    # Используем простую стратегию чанкования
    from yandex_cloud_ml_sdk.search_indexes import StaticIndexChunkingStrategy, VectorSearchIndexType

    op = sdk.search_indexes.create_deferred(
        uploaded_files,
        index_type=VectorSearchIndexType(
            chunking_strategy=StaticIndexChunkingStrategy(max_chunk_size_tokens=1000, chunk_overlap_tokens=100)
        ),
    )
    index = op.wait()
    print(f"Индекс создан. ID: {index.id}")

    print("6. Создание Ассистента...")
    # Создаем инструмент поиска по нашему индексу
    search_tool = sdk.tools.search_index(index)
    
    # Системный промпт для ассистента
    instruction = """
    Ты — вежливый и информативный ассистент приемной комиссии университета ИТМО.
    Твоя задача — отвечать на вопросы абитуриентов магистратуры на основе информации из твоей базы знаний (предоставленных документов).
    Отвечай только на основе найденной информации. НЕ придумывай ничего от себя.
    Если в документах нет ответа на вопрос, вежливо скажи, что не обладаешь такой информацией и предложи задать вопрос по-другому или обратиться в приемную комиссию.
    Структурируй ответы, используй списки, если это уместно.
    """
    
    assistant = sdk.assistants.create(
        model=sdk.models.completions("yandexgpt-lite"),  # Используем lite-модель
        instruction=instruction,
        tools=[search_tool]
    )
    print(f"Ассистент создан. ID: {assistant.id}")

    print("7. Сохранение конфигурации RAG...")
    rag_config = {
        "assistant_id": assistant.id,
        "search_index_id": index.id,
        "uploaded_file_ids": uploaded_file_ids
    }
    with open(RAG_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(rag_config, f, indent=2)
    
    print("Все ассеты успешно созданы и сконфигурированы!")

if __name__ == "__main__":
    main()

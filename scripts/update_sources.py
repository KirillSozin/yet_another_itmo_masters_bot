import os
import requests
from bs4 import BeautifulSoup
from typing import Dict

# Словарь, где ключ - URL, а значение - имя файла для сохранения
SOURCES = {
    "https://abit.itmo.ru/program/master/ai_product": "ai_product.txt",
    "https://abit.itmo.ru/program/master/ai": "ai.txt",
    "https://abit.itmo.ru/file_storage/file/pages/80/pravila_mag.pdf": "admission_rules.txt"
}

# Директория для сохранения текстовых файлов
OUTPUT_DIR = "data/source_texts"

def fetch_and_parse():
    """
    Скачивает и парсит веб-страницы, извлекая основной текстовый контент.
    Результат сохраняется в текстовые файлы.
    """
    print("Начинаю обновление исходных данных...")
    
    # Создаем директорию, если ее нет
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url, filename in SOURCES.items():
        try:
            print(f"Скачиваю: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()  # Проверка на ошибки HTTP (4xx, 5xx)
            
            soup = BeautifulSoup(response.content, 'html.parser')

            # Ищем основной контейнер с контентом. 
            # Этот селектор может потребовать обновления, если верстка сайта изменится.
            # На данный момент контент находится внутри <div data-controller="read-more">
            content_div = soup.find('div', attrs={'data-controller': 'read-more'})
            
            if not content_div:
                # Если основной блок не найден, попробуем найти тег <main>
                content_div = soup.find('main')
                if not content_div:
                    print(f"Не удалось найти основной блок контента для {url}")
                    continue

            # Извлекаем текст, используя разделитель для лучшей читаемости
            text = content_div.get_text(separator='\n', strip=True)
            
            # Сохраняем в файл
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Сохранено в: {filepath}")

        except requests.RequestException as e:
            print(f"Ошибка при скачивании {url}: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка при обработке {url}: {e}")

    print("Обновление исходных данных завершено.")

if __name__ == "__main__":
    fetch_and_parse()

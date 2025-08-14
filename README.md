# QA-ассистент для абитуриентов ИТМО

Телеграм-бот, который консультирует абитуриентов по магистерским программам на основе информации с официального сайта.

**➡️ Попробовать в Telegram: [@yet_another_itmo_qa_bot](https://t.me/yet_another_itmo_qa_bot)**

### 🛠️ Технологический стек

| Компонент        | Инструмент            |
| ---------------- | --------------------- |
| Язык             | Python 3.11+          |
| Telegram Framework| Aiogram 3             |
| AI-платформа     | Yandex Assistant API  |
| SDK              | yandex-cloud-ml-sdk   |
| Развертывание    | Docker                |

---

## 🚀 Быстрый старт

### Шаг 1: Клонирование и зависимости

```bash
git clone <URL_вашего_репозитория>
cd itmo_master_bot

# Рекомендуется использовать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Шаг 2: Настройка переменных окружения

Скопируйте файл-образец и впишите в него свои ключи.

```bash
cp .env.example .env
```
Содержимое `.env`:
```dotenv
# Токен вашего Telegram бота от @BotFather
BOT_TOKEN=...
# API-ключ сервисного аккаунта Yandex Cloud
YANDEX_API_KEY=...
# ID каталога (folder) в Yandex Cloud
YANDEX_FOLDER_ID=...
```

### Шаг 3: Создание RAG-ассетов в Yandex Cloud (Единоразово)

Этот скрипт **необходимо запустить один раз** перед первым запуском бота. Он скачает данные с сайтов, загрузит их в Yandex Cloud, создаст поисковый индекс и "Ассистента".

```bash
python -m scripts.create_rag_assets
```
После успешного выполнения в папке `data/` появится файл `rag_config.json`. Он нужен боту для работы.

---

## ▶️ Запуск бота

### Локальный запуск (для разработки)

```bash
python -m app.bot
```

### Запуск через Docker (для production)

1.  **Соберите Docker-образ:**
    ```bash
    docker build -t itmo-master-bot .
    ```

2.  **Запустите контейнер:**
    Эта команда запускает бота в фоновом режиме, автоматически перезапускает его в случае сбоя и передает внутрь необходимые конфигурационные файлы.

    ```bash
    docker run -d --name itmo-bot \
      --restart unless-stopped \
      --env-file .env \
      -v "$(pwd)/data/rag_config.json":/app/data/rag_config.json:ro \
      itmo-master-bot
    ```

---

## 🔄 Обновление базы знаний

Если информация на сайтах ИТМО изменилась:

1.  **Запустите снова скрипт** для пересоздания ассетов в Yandex Cloud. **Внимание:** это создаст *новые* ресурсы (индекс и ассистента) и перезапишет `data/rag_config.json`.
    ```bash
    python -m scripts.create_rag_assets
    ```
2.  **Перезапустите бота** (или Docker-контейнер), чтобы он подхватил новую конфигурацию из `rag_config.json`.
    ```bash
    docker restart itmo-bot
    ```


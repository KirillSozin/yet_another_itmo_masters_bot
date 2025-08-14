import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Settings:
    bot_token: str
    yandex_cloud_api_key: str
    yandex_folder_id: str

def load_config() -> Settings:
    load_dotenv()
    return Settings(
        bot_token=os.getenv("BOT_TOKEN"),
        yandex_cloud_api_key=os.getenv("YANDEX_CLOUD_API_KEY"),
        yandex_folder_id=os.getenv("YANDEX_FOLDER_ID")
    )

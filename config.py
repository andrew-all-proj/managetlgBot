from pathlib import Path

BASE_DIR = Path(__file__).parent
_USER_NAME_DB = "postgres"
_PASSWORD_DB = 1
_NAME_DB = "web_site"
PATH_FOR_MEDIA = 'D:\manager_tlg\/backend\/api_manager_tlg\content_media'
CONTENT_DIR = f'D:\manager_tlg\/backend\/api_manager_tlg\content_media'


class Config:
    SQLALCHEMY_DATABASE = f"postgresql+psycopg2://{_USER_NAME_DB}:{_PASSWORD_DB}@localhost/{_NAME_DB}"
    PATH_LOG_FILE = f"{BASE_DIR}/log_bot.log"
    PATH_FOR_MEDIA = PATH_FOR_MEDIA

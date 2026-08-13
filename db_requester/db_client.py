from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DataBaseCreds

USERNAME = DataBaseCreds.DB_USER
PASSWORD = DataBaseCreds.DB_PASSWORD
HOST = DataBaseCreds.DB_HOST
PORT = DataBaseCreds.DB_PORT
DATABASE_NAME = DataBaseCreds.DB_NAME

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=True  # Установить True для отладки SQL запросов
)

#  создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()
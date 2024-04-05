from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
load_dotenv()


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    eth_rpc: str = 'https://eth.drpc.org'

    notification_period: int = 10

    @property
    def db_url(self):
        return f'postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}' \
                f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'


settings: Settings = Settings()

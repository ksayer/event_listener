from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
load_dotenv()


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    contract_address: str = '0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0'
    abi_file: str = f'{BASE_DIR}/core/abi.json'
    event_name: str = 'TotalDistribution'
    eth_rpc: str = 'https://eth.drpc.org'
    main_loop_delay: int = 30

    notification_period: int = 60 * 60 * 4

    tg_token: str
    tg_chat_id: str

    @property
    def db_url(self):
        return f'postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}' \
                f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'


settings: Settings = Settings()

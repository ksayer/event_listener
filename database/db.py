from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.settings import settings

load_dotenv()


engine = create_engine(settings.db_url,)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

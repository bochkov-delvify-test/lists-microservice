from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from delvify.core import db_settings

engine = create_engine(url=db_settings.DB_URI, pool_pre_ping=True)  # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

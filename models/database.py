from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 資料庫連接資訊
DATABASE_URL = "postgresql://ticket_user:ticket_pass@localhost/ticketing_system"

# 建立資料庫引擎
engine = create_engine(DATABASE_URL)

# 建立 Session 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base 類別
Base = declarative_base()

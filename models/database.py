# models/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用現有的資料庫使用者（例如，postgres）

# 請根據您的資料庫設定更改以下變數
your_username = "postgres"
your_password = "1234"

DATABASE_URL = "postgresql://" + your_username + ":" + your_password + "@localhost:5432/ticketsystem"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

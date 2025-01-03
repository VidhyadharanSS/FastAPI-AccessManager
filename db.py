import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




# Database initialization
DATABASE_URL = 'sqlite:///./employee.db'  

# Engine creation
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# Session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base mapping
Base = declarative_base()

# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

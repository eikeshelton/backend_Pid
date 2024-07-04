from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://esfs:999178058Eike@projetopid.cjs6ku6kun0r.us-east-1.rds.amazonaws.com/projeto_pid"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import os
from sqlmodel import SQLModel, Session, create_engine

# Carrega a URL do banco a partir da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")  # ex.: 'postgresql://user:pass@db.projeto.supabase.co:5432/postgres?sslmode=require'
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

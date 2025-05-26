from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Curriculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    area_profissional: Optional[str]
    nivel_carreira: Optional[str]
    linkedin: Optional[str]
    curriculo_texto: str
    is_premium: bool = False
    data_envio: datetime = Field(default_factory=datetime.utcnow)

class Analise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    curriculo_id: int = Field(foreign_key="curriculo.id")
    resposta_json: str
    nota_geral: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


# cv_analyzer_backend.py

from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ---------------------------------------------------
#  Models
# ---------------------------------------------------

class TestAnswers(BaseModel):
    disc:       List[int]
    big_five:   List[int]
    emotional:  List[int]
    communication: List[int]
    focus:      List[int]

class CVPayload(BaseModel):
    nome:               str
    email:              str
    area_profissional:  Optional[str] = None
    nivel_carreira:     Optional[str] = None
    linkedin:           Optional[str] = None
    curriculo_texto:    str
    tipo_analise:       str
    respostas_teste:    TestAnswers

class CVResult(BaseModel):
    # Campos de exemplo — adapte ao que sua IA retorna
    nota_geral:           float
    pontos_fortes:        List[str]
    melhorias:            List[str]
    correcoes_portugues:  List[str]
    grafico:              Optional[str] = None  # URL ou base64 do gráfico (premium)
    recomendacoes:        Optional[List[str]] = None  # extra no premium

# ---------------------------------------------------
#  App & CORS
# ---------------------------------------------------

app = FastAPI(
    title="CurrículoPro API",
    description="API para análise gratuita e premium de currículos com testes simulados",
    version="1.0.0",
    docs_url="/docs",         # Swagger UI
    redoc_url="/redoc",       # ReDoc
)

# Ajuste os origins para o domínio do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://curriculoproai.com",
        "https://www.curriculoproai.com",
        # Se usar o domínio gerado pelo Horizons, acrescente aqui...
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
#  Endpoints
# ---------------------------------------------------

@app.post("/processar-cv", response_model=CVResult)
async def processar_cv(payload: CVPayload):
    """
    Recebe todos os dados do formulário (JSON), simula a
    análise e retorna o resultado.
    """
    # Aqui você colocaria sua lógica real, chamando OpenAI, analisando CV, etc.
    # Abaixo só estou simulando uma resposta:
    resultado = CVResult(
        nota_geral=  8.2 if payload.tipo_analise=="premium" else 7.5,
        pontos_fortes= [
            "Experiência relevante em tecnologia",
            "Boa clareza na comunicação"
        ],
        melhorias=[
            "Use mais verbos de ação",
            "Quantifique resultados"
        ],
        correcoes_portugues=[
            "'A nível de' → prefira 'Em nível de'"
        ],
        grafico=(
            "https://curriculoproai.com/static/graficos/analise.png"
            if payload.tipo_analise=="premium" else None
        ),
        recomendacoes=(
            ["Invista em networking", "Atualize seu LinkedIn"]
            if payload.tipo_analise=="premium" else None
        )
    )
    return resultado


# ---------------------------------------------------
#  Run (opcional, apenas para dev local)
# ---------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "cv_analyzer_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    return resultado

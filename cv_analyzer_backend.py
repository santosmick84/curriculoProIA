
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ---------------------------------------------------
#  Models
# ---------------------------------------------------

class TestAnswers(BaseModel):
    disc:           List[int]
    big_five:       List[int]
    emotional:      List[int]
    communication:  List[int]
    focus:          List[int]

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
    nota_geral:           float
    pontos_fortes:        List[str]
    melhorias:            List[str]
    correcoes_portugues:  List[str]
    grafico:              Optional[str] = None
    recomendacoes:        Optional[List[str]] = None

# ---------------------------------------------------
#  App & CORS
# ---------------------------------------------------

app = FastAPI(
    title="CurrículoPro API",
    description="API para análise gratuita e premium de currículos com testes simulados",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://curriculoproai.com",
        "https://www.curriculoproai.com",
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
    # Simulação de análise:
    is_premium = payload.tipo_analise == "premium"
    resultado = CVResult(
        nota_geral=8.5 if is_premium else 7.2,
        pontos_fortes=[
            "Experiência relevante detectada",
            "Boa organização das seções"
        ],
        melhorias=[
            "Quantifique resultados (ex: aumentei vendas em 20%)",
            "Aprimore o resumo profissional"
        ],
        correcoes_portugues=[
            "Evite 'A nível de'; prefira 'Em nível de'"
        ],
        grafico=("/static/graficos/analise-premium.png" if is_premium else None),
        recomendacoes=(
            ["Invista em networking LinkedIn", "Considere treinamento em gestão"]
            if is_premium else None
        )
    )
    return resultado

# ---------------------------------------------------
#  Main (para dev local)
# ---------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "cv_analyzer_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

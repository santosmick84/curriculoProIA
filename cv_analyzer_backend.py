import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import openai
from models import Curriculo, Analise
from db import init_db, get_session
from prompts import build_prompt
from dotenv import load_dotenv
openai.api_key = os.getenv("OPENAI_API_KEY")

# Carrega variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
# Inicializa o DB (cria tabelas se não existirem)
init_db()

# FastAPI setup
app = FastAPI(
    title="CurriculoProAI API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://curriculoproai.com",
        "https://www.curriculoproai.com",
        # se usar domínio Horizons, adicione aqui
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/processar-cv")
async def processar_cv(
    payload: Curriculo,
    session: Session = Depends(get_session)
):
    # 1) Salva submissão
    session.add(payload)
    session.commit()
    session.refresh(payload)

    # 2) Chama a OpenAI
    prompt = build_prompt(payload.curriculo_texto,
                           "premium" if payload.is_premium else "gratuita")
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
        )
    except Exception as e:
        raise HTTPException(502, detail="Erro ao chamar OpenAI")

    content = resp.choices[0].message.content
    try:
        analise_dict = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(500, detail="Resposta inválida da IA")

    # 3) Persiste análise
    an = Analise(
        curriculo_id=payload.id,
        resposta_json=content,
        nota_geral=analise_dict.get("nota_geral", 0)
    )
    session.add(an)
    session.commit()

    # 4) Retorna JSON da análise
    return analise_dict

# Para dev local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cv_analyzer_backend:app", host="0.0.0.0", port=8000, reload=True)

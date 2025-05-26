
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from typing import Optional

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for uploaded resumes
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Model for non-file fields
class CVRequest(BaseModel):
    nome: str
    email: str
    area: str
    nivel: str
    linkedin: Optional[str] = None
    texto_cv: Optional[str] = None
    is_premium: Optional[bool] = False

@app.post("/analisar-cv/")
async def analisar_cv(
    nome: str = Form(...),
    email: str = Form(...),
    area: str = Form(...),
    nivel: str = Form(...),
    linkedin: Optional[str] = Form(None),
    texto_cv: Optional[str] = Form(None),
    is_premium: Optional[bool] = Form(False),
    arquivo: Optional[UploadFile] = File(None)
):
    file_path = None
    if arquivo:
        file_location = os.path.join(UPLOAD_DIR, arquivo.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
        file_path = file_location

    # Simulated analysis
    resultado = {
        "nota": 7.8,
        "pontos_fortes": ["Clareza na apresentação", "Bom uso de verbos de ação"],
        "melhorias": ["Adicionar mais números ou resultados concretos", "Revisar a ortografia"],
        "correcoes_portugues": ["'A nível de' deve ser evitado"],
        "resumo_profissional": "Profissional com sólida experiência em [área], buscando [objetivo]...",
        "arquivo_recebido": file_path,
        "is_premium": is_premium
    }

    return resultado

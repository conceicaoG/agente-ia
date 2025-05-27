from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.cohere_service import CohereService
import pytz
import os

timezone = pytz.timezone("America/Sao_Paulo")
os.environ['TZ'] = 'America/Sao_Paulo'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Coloque sua chave aqui direto, só pra testar
API_KEY = "E0mHO1ZXzYYozABc4G1hdKu5JO1KKyZBeCCexco1"
service = CohereService(API_KEY)

@app.post("/chat")
def chat(req: ChatRequest):
    resposta = service.gerar_resposta(req.message)
    return {"resposta": resposta}

@app.post("/zerar_historico")
async def zerar_historico():
    service.zerar_historico()
    return {"mensagem": "Histórico zerado com sucesso!"}

@app.get("/")
def read_root():
    return {"mensagem": "Seu backend está funcionando 🎉"}
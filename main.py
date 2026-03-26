from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Importante
from scan import scan_pdf_wechat
import requests
import io

app = FastAPI()

# Permite que o Expo acesse as imagens
app.mount("/static", StaticFiles(directory="temp_images"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/escanear-pdf")
async def api_scan_pdf(file: UploadFile = File(...)):
    # ... (sua validação de PDF existente)
    conteudo_pdf = await file.read()
    resultado = scan_pdf_wechat(conteudo_pdf)
    return {"status": "sucesso", "data": resultado}

# Nova rota para testar o seu link do GitHub diretamente pelo Backend
@app.get("/testar-github")
async def testar_github():
    pdf_url = "https://raw.githubusercontent.com/AntonniSMoraes/acervo-pdfs/main/exemplo%20QR.pdf"
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao baixar PDF do GitHub")
    
    resultado = scan_pdf_wechat(response.content)
    return {"status": "sucesso", "data": resultado}

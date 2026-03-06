from fastapi import FastAPI, UploadFile, File, HTTPException
from scan import scan_pdf_wechat

app = FastAPI()

@app.get("/")
def inicio():
    return {"Localizador de QRs"}

@app.post("/escanear-pdf")
async def api_scan_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo enviado deve ser um PDF.")

    try:
        conteudo_pdf = await file.read()
        
        resultado = scan_pdf_wechat(conteudo_pdf)
        
        return {
            "status": "sucesso",
            "filename": file.filename,
            "data": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar: {str(e)}")
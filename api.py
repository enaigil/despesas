from fastapi import FastAPI
import os
import json
from google.oauth2.service_account import Credentials
import gspread

# Criar a aplicação FastAPI
app = FastAPI()

# Configurar escopos do Google
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Ler credenciais do Google via variável de ambiente
credenciais_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credenciais_json,
    scopes=scopes
)

# Conectar ao Google Sheets
gc = gspread.authorize(creds)
SPREADSHEET_NAME = "despesas"  # Nome da sua planilha
sh = gc.open(SPREADSHEET_NAME)
worksheet = sh.sheet1  # ou o nome da aba desejada

# Endpoints
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/despesas")
def criar_despesa(despesa: dict):
    try:
        worksheet.append_row([
            despesa["data"],
            despesa["despesa"],
            despesa["valor"],
            despesa["categoria"]
        ])
        return {"status": "ok"}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

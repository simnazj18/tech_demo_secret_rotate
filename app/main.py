from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.services import SecretScanner

app = FastAPI(title="Secrets Drift Dashboard")

# Setup Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize Scanner
scanner = SecretScanner(vault_url=settings.AZURE_KEYVAULT_URL)

@app.get("/")
async def dashboard(request: Request):
    data = scanner.get_dashboard_data()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "akv_secrets": data['akv_secrets'],
        "k8s_usage": data['k8s_usage'],
        "vault_url": settings.AZURE_KEYVAULT_URL
    })

@app.get("/api/scan")
async def scan():
    return scanner.get_dashboard_data()

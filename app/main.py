from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.llm_utils import call_mistral_featherless
import uvicorn

import os
import requests

from dotenv import load_dotenv
load_dotenv()

HF_API_TOKEN = os.getenv("HF_TOKEN")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def calculate_risk(age: int, miner: bool, hiv_positive: bool, tb_history: bool) -> int:
    score = 0
    if age > 50: score += 2
    if miner: score += 3
    if hiv_positive: score += 4
    if tb_history: score += 3
    return min(score, 10)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def load_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    age: int = Form(...),
    miner: bool = Form(False),
    hiv_positive: bool = Form(False),
    tb_history: bool = Form(False),
):
    risk_score = calculate_risk(age, miner, hiv_positive, tb_history)
    alert = "Cold chain check required!" if risk_score >= 7 else "Cold chain stable"
    return templates.TemplateResponse("result.html", {
        "request": request,
        "score": risk_score,
        "alert": alert
    })

@app.get("/summarize", response_class=HTMLResponse)
async def summarize_immunization(request: Request):
    hf_token = os.getenv("HF_API_TOKEN")

    prompt = (
        "Summarize how artificial intelligence and technology are transforming immunization "
        "campaigns, especially in low-resource or rural settings. Keep it under 150 words."
    )

    try:
        summary = call_mistral_featherless(prompt, hf_token)
    except Exception as e:
        summary = f"Error calling model: {str(e)}"

    return templates.TemplateResponse("summary.html", {
        "request": request,
        "summary": summary
    })

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

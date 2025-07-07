from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.llm_utils import ask_mistral
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

@app.get("/vaccine-chat", response_class=HTMLResponse)
async def vaccine_chat(request: Request):
    return templates.TemplateResponse("vaccine_chat.html", {"request": request})


@app.post("/vaccine-info", response_class=HTMLResponse)
async def vaccine_info(request: Request, topic: str = Form(...)):
    prompt = (
        f"Give a brief and clear explanation of the {topic.upper()} vaccine. "
        f"Include what it is, how it works, and who should get it."
    )

    try:
        response_text = ask_mistral(prompt)
    except Exception as e:
        response_text = f"Error generating response: {str(e)}"

    return templates.TemplateResponse("vaccine_response.html", {
        "request": request,
        "response": response_text
    })

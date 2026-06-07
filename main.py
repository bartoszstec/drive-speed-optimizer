from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fuzzy import calculate_safe_speed

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/safe-speed-form")
def safe_speed_form(
    visibility: float = Form(...),
    traffic: float = Form(...),
    vehicle_load: float = Form(...),
    road: float = Form(...)
):

    speed = calculate_safe_speed(
        visibility,
        traffic,
        vehicle_load,
        road
    )

    return {
        "safe_speed": round(speed, 2)
    }

@app.get("/oliwiery")
async def oliwiery():
    return {"message": "Hello Oliwier here"}
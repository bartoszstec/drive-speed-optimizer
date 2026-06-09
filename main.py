from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fuzzy import calculate_safe_speed

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/safe-speed-form", response_class=HTMLResponse)
def safe_speed_form(
    request: Request,
    visibility: float = Form(...),
    traffic: float = Form(...),
    vehicle_load: float = Form(...),
    road: float = Form(...)
):

    speed, chart = calculate_safe_speed(
        visibility,
        traffic,
        vehicle_load,
        road,
    )

    return templates.TemplateResponse(request=request, name="results.html", context={
            "safe_speed": round(speed),
            "visibility": round(visibility),
            "traffic": round(traffic),
            "vehicle_load": round(vehicle_load),
            "road": round(road),
            "chart": chart
        })

@app.get("/oliwiery")
async def oliwiery():
    return {"message": "Hello Oliwier here"}
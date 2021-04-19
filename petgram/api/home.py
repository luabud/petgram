from datetime import timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

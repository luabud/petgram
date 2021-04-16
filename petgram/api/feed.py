from fastapi import APIRouter, Depends
from petgram.api import crud
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()


@router.get("/feed")
def display_feed(user=Depends(crud.manager)):
    return templates.TemplateResponse("home.html", {"request": request})
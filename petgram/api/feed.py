from fastapi import APIRouter, Depends, Request, HTTPException
from petgram.api import crud
from fastapi.templating import Jinja2Templates
from main import app

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()


@router.get("/feed")
def display_feed(request: Request, user=Depends(crud.manager)):
    return templates.TemplateResponse("feed.html", {"request": request})

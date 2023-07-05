from datetime import timedelta
from os import access
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from petgram.api.exceptions import ERROR_IDS
import petgram.db as db
from petgram.api import home, users


app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"))


@app.on_event("startup")
async def startup():
    try:
        await db.database.connect()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        app.state.db = None


@app.on_event("shutdown")
async def shutdown():
    try:
        await db.database.disconnect()
    except Exception as e:
        print(f"Failed to disconnect to database: {e}")

# TODO: handle PasswordMismatchError case
@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    error_id = ERROR_IDS[exc.status_code]
    return RedirectResponse(url=f"/login?error={error_id}", status_code=exc.status_code)


app.include_router(users.router)
app.include_router(home.router)

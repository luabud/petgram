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


# @app.exception_handler(InvalidCredentialsException)
# async def invalid_credentials_exception_handler(
#     request: Request, exc: InvalidCredentialsException
# ):
#     return RedirectResponse(url="/login?error=invalid_credentials", status_code=401)


# @app.exception_handler(DatabaseAccessException)
# async def database_access_exception_handler(
#     request: Request, exc: DatabaseAccessException
# ):
#     return RedirectResponse(url="/login?error=database_error", status_code=303)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    error_id = ERROR_IDS[exc.status_code]
    return RedirectResponse(url="/login?error={error_id}", status_code=exc.status_code)


# ow whenever you want your user to be logged in to use a route, you can simply use your LoginManager instance as a dependency.

# @app.get('/protected')
# def protected_route(user=Depends(manager)):
#     ...


# user_id = await crud.post(payload)

# response_object = {
#     "id": user_id,
#     "username": payload.username,
#     "name": payload.name,
#     "bio": payload.bio,
# }
# return response_object

app.include_router(users.router)
app.include_router(home.router)

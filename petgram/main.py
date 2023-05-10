from datetime import timedelta
from os import access
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
import petgram.db as db
from petgram.api import home, users


app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"))


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


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

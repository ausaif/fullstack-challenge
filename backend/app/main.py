from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .routers import authentication, properties, users
from .shared.token import invalid_token

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
PREFIX = "/api/v0"


def verify_token(x_token: str = Header()):
    if invalid_token(x_token):
        raise HTTPException(status_code=401, detail="User is unauthorized")


app.include_router(authentication.router, prefix=PREFIX,
                   tags=["auth"],
                   dependencies=[],
                   )
app.include_router(properties.router, prefix=PREFIX,
                   tags=["properties"],
                   dependencies=[Depends(verify_token)],
                   )
app.include_router(users.router, prefix=f"{PREFIX}/users",
                   tags=["users"],
                   dependencies=[Depends(verify_token)],
                   )

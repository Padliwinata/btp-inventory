from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import auth
from exceptions import DependencyException


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(DependencyException)
async def custom_handler(exc: DependencyException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail_info
    )

app.include_router(auth.router)



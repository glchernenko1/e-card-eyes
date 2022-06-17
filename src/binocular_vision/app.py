from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .api import router

app = FastAPI()
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

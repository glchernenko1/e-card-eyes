from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .api import router

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация'
    },
    {
        'name': 'patient',
        'description': 'api для работы клиентской части пациентов'
    },
    {
      'name': 'doctor',
      'description':  'api для работы клиентской части доктора'
    }
]

app = FastAPI(
    title='binocular_vision',
    description='Электронная история болезни',
    version='1.0.0',
    openapi_tags=tags_metadata
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

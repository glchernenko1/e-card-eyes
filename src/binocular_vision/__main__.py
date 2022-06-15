import uvicorn

from .settings import settings

from .database import engine
from .db_table.table import Base

Base.metadata.create_all(engine)

uvicorn.run(
    'binocular_vision.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)



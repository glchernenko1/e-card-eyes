from fastapi.testclient import TestClient

from binocular_vision.app import app
from binocular_vision.database import engine, Session
from binocular_vision.db_table.table import Base

Base.metadata.create_all(engine)

client = TestClient(app)


def client_db_all():
    session = Session()
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


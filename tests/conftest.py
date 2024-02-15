# Archivo para las fixtures
from testingactions.user_db import DataBase
import pytest



@pytest.fixture(scope="session")
def db_conn():
    db = DataBase('mongodb://sertemo.db')
    db.create_collection('usuarios')
    return db
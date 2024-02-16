# Archivo para las fixtures
# Las fixtures que están aqui se comparten para todos los tests
from testingactions.user_db import DataBase
import pytest



@pytest.fixture(scope="session")
def db_conn():
    db = DataBase('mongodb://sertemo.db')
    db.create_collection('usuarios')
    return db
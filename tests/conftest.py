import pytest
from app.config import db
from app.utils import add_test_user


@pytest.fixture(scope="module", autouse=True)
def clear_db():
    yield None

    db['users'].drop()

@pytest.fixture(scope="module", autouse=True)
def seed():
    add_test_user()
import pytest

from server import create_app
from src.db.database import db


# @pytest.fixture(scope="function")
@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture
def client(app):
    app = create_app(db_connection='sqlite:///test.db')
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

    ctx = app.app_context()
    ctx.push()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

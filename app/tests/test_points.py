import os
import tempfile
import pytest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app import db
from app.astronauts.models import Astronaut

@pytest.fixture
def client():
    app=create_app()
    db_fd, dbconf = tempfile.mkstemp()
    db_uri = 'sqlite:///{}?check_same_thread=False'.format(dbconf)

    app.config['TESTING']=True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI']=db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()

        yield client

    os.close(db_fd)
    os.unlink(dbconf)


def test_create_astronaut(client):
    data={
	"firstName": "Ibrahim",
	"lastName": "Fielipo",
	"dateOfBirth": "10/11/1996",
	"superpower": "190IQ`",
}
    rv = client.post('/astronauts',json=data)
    rows = json.loads(rv.data)
    count = len(rows)
    assert rv.status_code  == 201, rv.data

def test_getAstronauts(client):
    rv = client.get('/astronauts')
    rows = json.loads(rv.data)
    count = len(rows)
    assert rv.status_code  == 200, rv.data
    assert count == 1, rv.data

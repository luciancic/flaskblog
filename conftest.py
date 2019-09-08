'''Makes the tester available in all inheriting test cases'''

import pytest
from flaskblog.config.base import TestConfig
from flaskblog import create_app, db


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.drop_all()

import os

from fastapi.testclient import TestClient

from app.db.sqlite_database import DBConfig, setup_schema, add_user, __execute_script
from app.main import app, PREFIX
from app.models.user import UserSignUp


def setup_database():
    db_name = "enodo-test.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    DBConfig.db_name = db_name
    setup_schema()
    add_user(UserSignUp(username="johndoe", password="testpassword", firstname="John", lastname="Doe",
                        email="johndoe@example.com"))
    __execute_script("""
    BEGIN;
    insert into class values (211, 'Two to Six Apartments, Over 62 Years');
    insert into class values (212, 'Mixed commercial/residential building, 6 units or less, sq ft less than 20,000');
    insert into property values ('68643f98-173c-4109-9fbf-501ab6fd42d1', '210 N JUSTINE ST, CHICAGO, IL',
    595820, 211, 'Multi Family', 3007.0);
    insert into property values ('7f9f77af-79de-4038-89ac-cb34b2df0e71', '1529 W TAYLOR ST, CHICAGO, IL',
    1302750, 212, 'Multi Family', 14243.0);
    COMMIT;
    """)


setup_database()
client = TestClient(app)


def test_authentication_for_valid_user():
    response = client.post(f"{PREFIX}/login", json={
        "username": "johndoe",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'x-token' in response.json()


def test_authentication_for_invalid_user():
    response = client.post(f"{PREFIX}/login", json={
        "username": "fakejohndoe",
        "password": "fakepassword"
    })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "User is unauthorized"
    }


def test_user_registration():
    response = client.post(f"{PREFIX}/register", json={
        "username": "janedoe",
        "password": "testpassword",
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "janedoe@example.com"
    })
    assert response.status_code == 201
    assert 'x-token' in response.json()


def test_list_of_properties():
    response = client.post(f"{PREFIX}/login", json={
        "username": "johndoe",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'x-token' in response.json()
    x_token = response.json()['x-token']

    response = client.get(f"{PREFIX}/properties", headers={"X-Token": x_token})
    assert response.status_code == 200
    assert response.json()['total_count'] == 2

    response = client.get(f"{PREFIX}/properties", params={'full_address': "N JUSTINE ST"}, headers={"X-Token": x_token})
    assert response.status_code == 200
    assert response.json()['total_count'] == 1

    response = client.get(f"{PREFIX}/properties", params={'full_address': "Non existent address"},
                          headers={"X-Token": x_token})
    assert response.status_code == 200
    assert response.json()['total_count'] == 0


def test_add_user_property():
    response = client.post(f"{PREFIX}/login", json={
        "username": "johndoe",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'x-token' in response.json()
    x_token = response.json()['x-token']

    response = client.post(f"{PREFIX}/users/properties", params={'property_id': "7f9f77af-79de-4038-89ac-cb34b2df0e71"},
                           headers={"X-Token": x_token})
    assert response.status_code == 201
    assert response.json() == {'message': 'Property added'}

    response = client.get(f"{PREFIX}/users/properties",
                          headers={"X-Token": x_token})
    assert response.status_code == 200
    assert len(response.json()['data']) == 1


def test_remove_user_property():
    response = client.post(f"{PREFIX}/login", json={
        "username": "johndoe",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'x-token' in response.json()
    x_token = response.json()['x-token']

    response = client.delete(f"{PREFIX}/users/properties/7f9f77af-79de-4038-89ac-cb34b2df0e71",
                             headers={"X-Token": x_token})
    assert response.status_code == 200
    assert response.json() == {'message': 'Property removed'}

    response = client.get(f"{PREFIX}/users/properties",
                          headers={"X-Token": x_token})
    assert response.status_code == 200
    assert response.json()['data'] == []

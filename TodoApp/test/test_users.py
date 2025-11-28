from .utils import *
from ..routers.users import get_current_user
from ..database import get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "CheekyDave"
    assert response.json()["email"] == "dave@example.com"
    assert response.json()["first_name"] == "Dave"
    assert response.json()["last_name"] == "Cheeky"
    assert response.json()["phone_number"] == "1111111111"
    assert response.json()["role"] == "admin"


def test_change_password_success(test_user):
    response = client.put("/users/password", json={"password": "testpassword",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_password(test_user):
    response = client.put("/users/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}

def test_change_phone_number_success(test_user):
    response = client.put("/users/phone_number", json={"phone_number":"22222222222222"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
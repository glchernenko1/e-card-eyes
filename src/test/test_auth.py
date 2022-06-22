from fastapi.security import OAuth2PasswordRequestForm

from main import client, client_db_all


def test_sing_up_doctor_correct():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    assert response.status_code == 200


def test_sing_up_doctor_login_exists():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user1@example.com",
            "password": "testtest"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Логин уже используется'}


def test_sing_up_doctor_email_exists():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test1",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email уже зарегистрирован'}


def test_sing_up_doctor_password_les_8():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test1",
            "email": "user@example.com",
            "password": "2"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "Пароль должен быть от 8 символов",
                "type": "value_error"
            }
        ],
        "body": {
            "full_name": "test",
            "login": "test1",
            "email": "user@example.com",
            "password": "2"
        }
    }


def test_sing_up_doctor_invalid_email():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test1",
            "email": "userexample.com",
            "password": "testtest"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ],
        "body": {
            "full_name": "test",
            "login": "test1",
            "email": "userexample.com",
            "password": "testtest"
        }
    }


def test_sing_up_doctor_not_correct_input_json():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full1_name": "test",
            "login1": "test",
            "email2": "user@example.com",
            "pass2word": "testtest"
        }
    )
    assert response.status_code == 422


def test_sing_in_doctor_correct():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        'auth/sing_in_doctor',
        data={"username": "test", "password": "testtest"},

    )
    assert response.status_code == 200


def test_sing_in_doctor_fail_password():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        'auth/sing_in_doctor',
        data={"username": "test", "password": "testtest1"},

    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль"
    }


def test_sing_in_doctor_fail_login():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test",
            "login": "test",
            "email": "user@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        'auth/sing_in_doctor',
        data={"username": "test1", "password": "testtest"},

    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль"
    }


def test_sing_in_patient_correct():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test1",
            "login": "test1",
            "email": "user1@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "test1", "password": "testtest"},

    )
    token = response.json()['access_token']

    response1 = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},
    )
    assert response.status_code == 200


def test_sing_in_patient_fail_password():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test1",
            "login": "test1",
            "email": "user1@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "test1", "password": "testtest"},

    )
    token = response.json()['access_token']

    response1 = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string2"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль"
    }


def test_sing_in_patient_fail_login():
    client_db_all()
    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test1",
            "login": "test1",
            "email": "user1@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "test1", "password": "testtest"},

    )
    token = response.json()['access_token']

    response1 = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string1", "password": "string"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль"
    }
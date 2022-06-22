from main import client, client_db_all


def test_patient():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.get(
        '/patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
    )

    assert response.status_code == 401

    response = client.get(
        '/patient',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
    )
    assert response.status_code == 200
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': response.json()['id'],
                               'login': 'string',
                               'tasks': []}


def test_get_current_task():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.get(
        '/patient/get_current_task',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
    )

    assert response.status_code == 401

    response = client.get(
        '/patient/get_current_task',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
    )
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json=[
            {
                "task": "classic",
                "quantity": 0
            },
            {
                "task": "no_classic",
                "quantity": 0
            },
        ]
    )

    assert response.status_code == 200

    response = client.get(
        '/patient/get_current_task',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
    )
    assert response.status_code == 200
    json = response.json()
    assert response.json() == [{'id': json[0]['id'], 'quantity': 0, 'task': 'classic'},
                               {'id': json[1]['id'], 'quantity': 0, 'task': 'no_classic'}]


def test_create_progress_one_iteration():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.post(
        '/patient/create_progress_one_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )

    assert response.status_code == 200
    assert response.json() == 'ok'


def test_add_list_progress():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.post(
        '/patient/create_progress_one_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia",
                "progress_value": 3
            },
            {
                "progress_type": "exotropia",
                "progress_value": 4
            },
        ]
    )

    assert response.status_code == 200

    response = client.post(
        '/patient/create_progress_one_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia",
                "progress_value": 2
            },
            {
                "progress_type": "exotropia",
                "progress_value": 1
            },
        ]
    )
    assert response.status_code == 200

    assert response.json() == 'ok'

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia",
                "progress_value": 2
            },
            {
                "progress_type": "exotropia",
                "progress_value": 1
            },
        ]
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'В одну сессию невозможно записать одинаковые типы'}

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia2",
                "progress_value": 2
            },
            {
                "progress_type": "exotropia",
                "progress_value": 1
            },
        ]
    )
    assert response.status_code == 422


def test_change_password():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.patch(
        '/patient/change_password',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json={
            "password": "string",
            "new_password": "new_password"
        }
    )
    assert response.status_code == 200

    token_patient = response.json()['access_token']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "new_password"},

    )
    assert response.status_code == 200

    response = client.patch(
        '/patient/change_password',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json={
            "password": "string1",
            "new_password": "new_password"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Неверный пароль'}


def test_statistic_two_end():
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
    token_doctor = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        '/auth/sing_in_patient',
        data={"username": "string", "password": "string"},

    )

    token_patient = response.json()['access_token']

    response = client.post(
        '/patient/create_progress_one_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia",
                "progress_value": 3
            },
            {
                "progress_type": "exotropia",
                "progress_value": 4
            },
        ]
    )

    response = client.get(
        f'/patient/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Нехватает данных'}

    response = client.post(
        '/patient/create_progress_one_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )
    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "esotropia",
                "progress_value": 2
            }]
    )

    response = client.get(
        f'/patient/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )
    assert response.status_code == 200
    assert response.json() == [{'progress_type': 'esotropia', 'progress_value': -1}]

    response = client.post(
        '/patient/add_list_progress_to_last_iteration',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json=[
            {
                "progress_type": "exotropia",
                "progress_value": 4
            }]
    )

    response = client.get(
        f'/patient/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_patient}",
        }
    )
    assert response.status_code == 200
    assert response.json() == [{'progress_type': 'esotropia', 'progress_value': -1},
                               {'progress_type': 'exotropia', 'progress_value': 0}]

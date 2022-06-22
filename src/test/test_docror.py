from main import client, client_db_all


def test_create_patient():
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

    response = client.post(
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

    assert response.status_code == 200

    resp = response.json()

    assert response.json() == {
        "full_name": "string",
        "login": "string",
        "full_name_current_dockter": "test1",
        "correct_diagnosis": None,
        "confirmed_diagnosis": None,
        "id": resp['id'],
        "tasks": []
    }


def test_create_patient_login_exists():
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

    response = client.post(
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

    assert response.status_code == 400

    assert response.json() == {'detail': 'Логин уже используется'}


def test_create_patient_without_token():
    client_db_all()

    response = client.post(
        '/doctor/sing_up_patient',

        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_patient_with_patient_token():
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

    token_patient = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_doctor():
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

    response = client.get(
        '/doctor',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    json = response.json()
    assert json == {
        "full_name": "test1",
        "login": "test1",
        "email": "user1@example.com",
        "id": json['id']
    }


def test_get_doctor_not_auth():
    response = client.get(
        '/doctor',
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_doctor_with_patient_token():
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

    token_patient = response.json()['access_token']

    response = client.get(
        '/doctor',
        headers={
            "Authorization": f"Bearer {token_patient}",
        },
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not enough permissions'}


def test_doctor_list_patient_and_list_patient():
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

    response = client.post(
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
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string1',
            'password': 'string',
        }
    )

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string2',
            'password': 'string',
        }
    )

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string3',
            'password': 'string',
        }
    )

    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "test12",
            "login": "test12",
            "email": "user12@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "test12", "password": "testtest"},

    )
    token_2 = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token_2}",
        },
        json={
            'full_name': 'string',
            'login': 'string4',
            'password': 'string',
        }
    )

    response = client.get(
        'doctor/doctor_list_patient/1?size=3',
        headers={
            "Authorization": f"Bearer {token_2}",
        },
    )
    json = response.json()
    assert response.status_code == 200
    assert response.json() == {'page': 1,
                               'patient_list': [{'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test12',
                                                 'id': json['patient_list'][0]['id'],
                                                 'login': 'string4',
                                                 'tasks': []}],
                               'size': 3,
                               'total': 1}
    response = client.get(
        'doctor/doctor_list_patient/1?size=2',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    json = response.json()
    assert response.status_code == 200
    assert response.json() == {'page': 1,
                               'patient_list': [{'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][0]['id'],
                                                 'login': 'string3',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][1]['id'],
                                                 'login': 'string2',
                                                 'tasks': []}],
                               'size': 2,
                               'total': 2}

    response = client.get(
        'doctor/doctor_list_patient/2?size=3',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    json = response.json()
    assert response.status_code == 200
    assert response.json() == {'page': 2,
                               'patient_list': [{'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][0]['id'],
                                                 'login': 'string',
                                                 'tasks': []}],
                               'size': 3,
                               'total': 2}

    response = client.get(
        'doctor/doctor_list_patient/4?size=3',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 404

    response = client.get(
        'doctor/list_patient/1?size=5',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    json = response.json()
    assert response.status_code == 200
    assert response.json() == {'page': 1,
                               'patient_list': [{'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test12',
                                                 'id': json['patient_list'][0]['id'],
                                                 'login': 'string4',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][1]['id'],
                                                 'login': 'string3',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][2]['id'],
                                                 'login': 'string2',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][3]['id'],
                                                 'login': 'string1',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][4]['id'],
                                                 'login': 'string',
                                                 'tasks': []}],
                               'size': 5,
                               'total': 1}

    response = client.get(
        'doctor/list_patient/1?size=5',
        headers={
            "Authorization": f"Bearer {token_2}",
        },
    )
    json = response.json()
    assert response.status_code == 200
    assert response.json() == {'page': 1,
                               'patient_list': [{'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test12',
                                                 'id': json['patient_list'][0]['id'],
                                                 'login': 'string4',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][1]['id'],
                                                 'login': 'string3',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][2]['id'],
                                                 'login': 'string2',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][3]['id'],
                                                 'login': 'string1',
                                                 'tasks': []},
                                                {'confirmed_diagnosis': None,
                                                 'correct_diagnosis': None,
                                                 'full_name': 'string',
                                                 'full_name_current_dockter': 'test1',
                                                 'id': json['patient_list'][4]['id'],
                                                 'login': 'string',
                                                 'tasks': []}],
                               'size': 5,
                               'total': 1}
    response = client.get(
        'doctor/list_patient/2?size=5',
        headers={
            "Authorization": f"Bearer {token_2}",
        },
    )
    assert response.status_code == 404


def test_search_patient_full_name():
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

    response = client.post(
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
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string1',
            'password': 'string',
        }
    )

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string1',
            'login': 'string2',
            'password': 'string',
        }
    )

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string3',
            'password': 'string',
        }
    )

    response = client.get(
        '/doctor/search_patient_full_name?patient_name=ss',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/doctor/search_patient_full_name?patient_name=string1',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    json = response.json()
    assert response.json() == [{'confirmed_diagnosis': None,
                                'correct_diagnosis': None,
                                'full_name': 'string1',
                                'full_name_current_dockter': 'test1',
                                'id': json[0]['id'],
                                'login': 'string2',
                                'tasks': []}]

    response = client.get(
        '/doctor/search_patient_full_name?patient_name=StrIng',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    json = response.json()
    assert response.json() == [{'confirmed_diagnosis': None,
                                'correct_diagnosis': None,
                                'full_name': 'string',
                                'full_name_current_dockter': 'test1',
                                'id': json[0]['id'],
                                'login': 'string',
                                'tasks': []},
                               {'confirmed_diagnosis': None,
                                'correct_diagnosis': None,
                                'full_name': 'string',
                                'full_name_current_dockter': 'test1',
                                'id': json[1]['id'],
                                'login': 'string1',
                                'tasks': []},
                               {'confirmed_diagnosis': None,
                                'correct_diagnosis': None,
                                'full_name': 'string',
                                'full_name_current_dockter': 'test1',
                                'id': json[2]['id'],
                                'login': 'string3',
                                'tasks': []}]


def test_search_patient_login():
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

    response = client.post(
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
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            'full_name': 'string',
            'login': 'string1',
            'password': 'string',
        }
    )
    response = client.get(
        '/doctor/search_patient_login?patient_login=ss',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/doctor/search_patient_login?patient_login=string1',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    json = response.json()
    assert response.json() == [{'confirmed_diagnosis': None,
                                'correct_diagnosis': None,
                                'full_name': 'string',
                                'full_name_current_dockter': 'test1',
                                'id': json[0]['id'],
                                'login': 'string1',
                                'tasks': []}]


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
    token = response.json()['access_token']

    response = client.patch(
        'doctor/change_password',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "old_password": "testtest1",
            "new_password": "testtest"
        }
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Неверный пароль'}

    response = client.patch(
        'doctor/change_password',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "old_password": "testtest",
            "new_password": "tes"
        }
    )
    assert response.status_code == 422

    response = client.patch(
        'doctor/change_password',
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "old_password": "testtest",
            "new_password": "testtest1"
        }
    )

    assert response.status_code == 200

    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "test1", "password": "testtest1"},
    )

    assert response.status_code == 200




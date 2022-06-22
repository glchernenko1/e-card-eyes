from main import client, client_db_all


def test_doctor_patient():
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

    id_patient = response.json()['id']

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
        f'doctor/patient/{id_patient}',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': id_patient,
                               'login': 'string',
                               'tasks': []}

    response = client.get(
        f'doctor/patient/0',
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 404


def test_update_correct_diagnosis():
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
    token1 = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.patch(
        f'/doctor/patient/{id_patient}',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "correct_diagnosis": "Здоров",
            "confirmed_diagnosis": True
        }
    )
    assert response.status_code == 200
    assert response.json() == {'confirmed_diagnosis': True,
                               'correct_diagnosis': 'Здоров',
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': id_patient,
                               'login': 'string',
                               'tasks': []}

    response = client.patch(
        f'/doctor/patient/0',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "correct_diagnosis": "Здоров",
            "confirmed_diagnosis": True
        }
    )
    assert response.status_code == 404

    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "newTest",
            "login": "newTest",
            "email": "user12@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "newTest", "password": "testtest"},

    )
    token1 = response.json()['access_token']

    response = client.patch(
        f'/doctor/patient/{id_patient}',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "correct_diagnosis": "Заболел",
            "confirmed_diagnosis": False
        }
    )
    assert response.status_code == 200
    assert response.json() == {'confirmed_diagnosis': False,
                               'correct_diagnosis': 'Заболел',
                               'full_name': 'string',
                               'full_name_current_dockter': 'newTest',
                               'id': id_patient,
                               'login': 'string',
                               'tasks': []}


def test_add_medical_history():
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
    token1 = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        f'doctor/patient/{id_patient}/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": "Почти здоров"
        }
    )
    assert response.status_code == 200
    json = response.json()
    assert response.json() == {'date': json['date'],
                               'doctor': 'test1',
                               'id': json["id"],
                               'patient_id': json["patient_id"],
                               'text': 'Почти здоров'}

    response = client.post(
        f'doctor/patient/0/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": "Почти здоров"
        }
    )
    assert response.status_code == 404

    response = client.post(
        '/auth/sign_up_doctor',
        json={
            "full_name": "newTEst",
            "login": "newTEst",
            "email": "user12@example.com",
            "password": "testtest"
        }
    )
    response = client.post(
        '/auth/sing_in_doctor',
        data={"username": "newTEst", "password": "testtest"},

    )
    token1 = response.json()['access_token']

    response = client.post(
        f'doctor/patient/{id_patient}/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": "Почти здоров2"
        }
    )

    assert response.status_code == 200
    json = response.json()
    assert response.json() == {'date': json['date'],
                               'doctor': 'newTEst',
                               'id': json["id"],
                               'patient_id': json["patient_id"],
                               'text': 'Почти здоров2'}

    response = client.get(
        f'doctor/patient/{id_patient}',
        headers={
            "Authorization": f"Bearer {token1}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'newTEst',
                               'id': id_patient,
                               'login': 'string',
                               'tasks': []}


def test_get_medical_history():
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
    token1 = response.json()['access_token']

    response = client.post(
        '/doctor/sing_up_patient',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            'full_name': 'string',
            'login': 'string',
            'password': 'string',
        }
    )

    id_patient = response.json()['id']

    response = client.post(
        f'doctor/patient/{id_patient}/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": "Почти здоров"
        }
    )
    response = client.post(
        f'doctor/patient/{id_patient}/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": " Также  здоров"
        }
    )
    response = client.post(
        f'doctor/patient/{id_patient}/medical_history',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json={
            "text": " Все ещё здоров"
        }
    )
    response = client.get(
        f'doctor/patient/{id_patient}/medical_history/1?size=2',
        headers={
            "Authorization": f"Bearer {token1}",
        },
    )
    assert response.status_code == 200
    json = response.json()
    assert json == {'medical_history_list':
                        [{'date': json['medical_history_list'][0]['date'],
                          'doctor': 'test1',
                          'id': json['medical_history_list'][0]['id'],
                          'patient_id': json['medical_history_list'][0]['patient_id'],
                          'text': ' Все ещё здоров'},
                         {'date': json['medical_history_list'][1]['date'],
                          'doctor': 'test1',
                          'id': json['medical_history_list'][1]['id'],
                          'patient_id': json['medical_history_list'][1]['patient_id'],
                          'text': ' Также  здоров'}],
                    'page': 1,
                    'size': 2,
                    'total': 2}
    response = client.get(
        f'doctor/patient/{id_patient}/medical_history/3?size=2',
        headers={
            "Authorization": f"Bearer {token1}",
        },
    )
    assert response.status_code == 404
    response = client.get(
        f'doctor/patient/{id_patient}/medical_history/2?size=2',
        headers={
            "Authorization": f"Bearer {token1}",
        },
    )
    assert response.status_code == 200
    json = response.json()
    assert json == {'medical_history_list':
                        [{'date': json['medical_history_list'][0]['date'],
                          'doctor': 'test1',
                          'id': json['medical_history_list'][0]['id'],
                          'patient_id': json['medical_history_list'][0]['patient_id'],
                          'text': 'Почти здоров'}],
                    'page': 2,
                    'size': 2,
                    'total': 2}

    response = client.get(
        f'doctor/patient/0/medical_history/3?size=2',
        headers={
            "Authorization": f"Bearer {token1}",
        },
    )
    assert response.status_code == 404

def test_
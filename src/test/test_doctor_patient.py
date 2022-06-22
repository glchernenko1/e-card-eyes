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


def test_add_task():
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
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
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
    json = response.json()
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': json['id'],
                               'login': 'string',
                               'tasks': [{'id': json['tasks'][0]['id'], 'quantity': 0, 'task': 'classic'},
                                         {'id': json['tasks'][1]['id'], 'quantity': 0, 'task': 'no_classic'}]}

    response = client.post(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
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
    json = response.json()
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': json['id'],
                               'login': 'string',
                               'tasks': [{'id': json['tasks'][0]['id'], 'quantity': 0, 'task': 'classic'},
                                         {'id': json['tasks'][1]['id'], 'quantity': 0, 'task': 'no_classic'},
                                         {'id': json['tasks'][2]['id'], 'quantity': 0, 'task': 'classic'},
                                         {'id': json['tasks'][3]['id'], 'quantity': 0, 'task': 'no_classic'}
                                         ]}

    response = client.post(
        f'doctor/patient/0/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[
            {
                "task": "classic",
                "quantity": 0
            }
        ]
    )
    assert response.status_code == 404

    response = client.post(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[
            {
                "task": "classic1",
                "quantity": 0
            }
        ]
    )
    assert response.status_code == 422


def test_del_task():
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
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[
            {
                "task": "classic",
                "quantity": 0
            },
            {
                "task": "no_classic",
                "quantity": 2
            },
            {
                "task": "no_classic",
                "quantity": 4
            },
        ]
    )
    json = response.json()
    id_list_del = [id['id'] for id in json['tasks']]

    response = client.delete(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=id_list_del
    )
    assert response.status_code == 200

    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': response.json()['id'],
                               'login': 'string',
                               'tasks': []}

    response = client.post(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[
            {
                "task": "classic",
                "quantity": 0
            },
            {
                "task": "no_classic",
                "quantity": 2
            },
            {
                "task": "no_classic",
                "quantity": 4
            },
        ]
    )
    json = response.json()
    id_list_del = [id['id'] for id in json['tasks']]

    response = client.delete(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[id_list_del[0]]
    )
    assert response.status_code == 200
    json = response.json()
    assert response.json() == {'confirmed_diagnosis': None,
                               'correct_diagnosis': None,
                               'full_name': 'string',
                               'full_name_current_dockter': 'test1',
                               'id': json['id'],
                               'login': 'string',
                               'tasks': [{'id': json['tasks'][0]['id'], 'quantity': 2, 'task': 'no_classic'},
                                         {'id': json['tasks'][1]['id'], 'quantity': 4, 'task': 'no_classic'}]}

    response = client.delete(
        f'doctor/patient/{id_patient}/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[id_list_del[2], 0]
    )

    assert response.status_code == 404

    response = client.delete(
        f'doctor/patient/0/tasks',
        headers={
            "Authorization": f"Bearer {token1}",
        },
        json=[id_list_del[1]]
    )
    assert response.status_code == 404


def test_patient_progress():
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

    #####################################
    response = client.get(
        f'/doctor/patient/{id_patient}/progress/1?size=1',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )
    assert response.status_code == 200
    json = response.json()
    assert json == {'page': 1,
                    'progress_patient_one_iteration_list':
                        [{'date': json['progress_patient_one_iteration_list'][0]['date'],
                          'id': json['progress_patient_one_iteration_list'][0]['id'],
                          'progress': [
                              {'id': json['progress_patient_one_iteration_list'][0]['progress'][0]['id'],
                               'progress_type': 'esotropia',
                               'progress_value': 2},
                              {'id': json['progress_patient_one_iteration_list'][0]['progress'][1]['id'],
                               'progress_type': 'exotropia',
                               'progress_value': 1}]}],
                    'size': 1,
                    'total': 2}
    response = client.get(
        f'/doctor/patient/{id_patient}/progress/3?size=1',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )
    assert response.status_code == 404

    response = client.get(
        f'/doctor/patient/0/progress/1?size=1',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )
    assert response.status_code == 404


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

    #############

    response = client.get(
        f'/doctor/patient/{id_patient}/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Нехватает данных'}

    #############

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

    response = client.get(
        f'/doctor/patient/{id_patient}/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )

    assert response.status_code == 200
    assert response.json() == [{'progress_type': 'esotropia', 'progress_value': -1},
                               {'progress_type': 'exotropia', 'progress_value': -3}]

    response = client.get(
        f'/doctor/patient/0/statistic_two_end',
        headers={
            "Authorization": f"Bearer {token_doctor}",
        }
    )

    assert response.status_code == 404

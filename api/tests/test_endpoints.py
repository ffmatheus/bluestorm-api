from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import text, orm
from sqlmodel import MetaData, Table
from api.main import app
from api.database import engine



client = TestClient(app)


class TestDB:

    def test_db(self):

        connection = engine.connect()
        results = connection.execute(text('SELECT * FROM PATIENTS'))
        row = results.fetchone()

    def test_db_sqlmodel(self):
        
        table1meta = MetaData(engine)
        table1 = Table('PATIENTS', table1meta, autoload=True)
        DBSession = orm.sessionmaker(bind=engine)
        session = DBSession()

        results = session.query(table1).all()
        assert len(results) > 20


class TestBaseAuth:
        
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "USERNAME": "matheus",
        "PASSWORD": "teste"
    }
    response = client.post(
        "/login",
        json=data)

    headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + response.json()["token"]
        }
    print(headers)


class TestApiGet(TestBaseAuth):

    def test_read_all_patients(self):
        
        response = client.get(
            "/patients",
            headers=TestBaseAuth.headers)
        assert response.status_code == 200
        assert len(response.json()) > 20
    
    def test_read_all_pharmacies(self):
        
        response = client.get(
            "/pharmacies",
            headers=TestBaseAuth.headers)
        assert response.status_code == 200
        assert len(response.json()) > 8
    
    def test_read_all_transactions(self):
        
        response = client.get(
            "/transactions",
            headers=TestBaseAuth.headers)
        assert response.status_code == 200
        assert len(response.json()) > 200


class TestApiPost(TestBaseAuth):

    def test_create_patient(self):

        data = {
            "FIRST_NAME": "Test",
            "LAST_NAME": "Testing",
            "DATE_OF_BIRTH": "2022-08-07T04:38:55.573Z"
        }
        response = client.post(
            "/patients",
            headers=TestBaseAuth.headers,
            json=data)
        assert response.status_code == 201
    
    def test_create_pharmacy(self):

        data = {
            "NAME": "Test",
            "CITY": "Testing"
        }
        response = client.post(
            "/pharmacies",
            headers=TestBaseAuth.headers,
            json=data)
        assert response.status_code == 201
    
    def test_create_transaction(self):

        data = {
            "PATIENT_UUID": "PATIENT0045",
            "PHARMACY_UUID": "PHARM0008",
            "AMOUNT": 54.0,
            "TIMESTAMP": "2022-08-07T04:38:55.573Z"
        }
        response = client.post(
            "/transactions",
            headers=TestBaseAuth.headers,
            json=data)
        assert response.status_code == 201

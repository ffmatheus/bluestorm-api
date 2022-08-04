from fastapi.testclient import TestClient
from sqlalchemy import text, orm
from sqlmodel import MetaData, Table
from main import app
from database import engine


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


class TestApiGet:

    def test_login(self):
        
        
        response = app.post(
            "/login",
            data = {
            "USERNAME": "matheus",
            "PASSWORD": "teste"
        })
        assert response.status_code == 200

    def test_read_all_patients(self):
        
        response = client.get("/patients")
        print(response.json())
        assert response.status_code == 200
        assert len(response) > 20
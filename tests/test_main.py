import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from API_Commandes.main import app
from API_Commandes.database import Base, get_db
import API_Commandes.models 

# Configuration de la base de données de test PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/Commandes_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override la dépendance get_db pour utiliser la base de données de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configuration de la base de données avant de lancer les tests
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Nettoyage de la base de données après les tests
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Crée une nouvelle session de test pour chaque test
        self.db = TestingSessionLocal()

    def tearDown(self):
        # Ferme la session de test après chaque test
        self.db.close()

    def test_create_commande(self):
        response = client.post(
            "/customers/orders",
            json={
                "clientId": 1,
                "produits": [{"produitId": 1}, {"produitId": 2}]
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["clientId"], 1)
        self.assertEqual(len(data["produits"]), 2)

    def test_read_commande(self):
        # Crée plusieurs commandes
        client.post(
            "/customers/orders",
            json={
                "clientId": 1,
                "produits": [{"produitId": 1}, {"produitId": 2}]
            },
        )
        client.post(
            "/customers/orders",
            json={
                "clientId": 1,
                "produits": [{"produitId": 3}]
            },
        )

        # Maintenant teste la récupération des commandes
        response = client.get(f"/customers/1/orders")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["clientId"], 1)
        self.assertEqual(data[1]["clientId"], 1)

        # Teste un client sans commande
        response = client.get("/customers/999/orders")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Commandes not found"})

if __name__ == "__main__":
    unittest.main()

import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from API_Commandes.main import app
from API_Commandes.database import Base, get_db
import os
from dotenv import load_dotenv
import aio_pika
import time
import asyncio

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def wait_for_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            await connection.close()
            break
        except Exception:
            print("Waiting for RabbitMQ...")
            time.sleep(5)


# Configuration du client de test pour utiliser la base de données de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class CommmandesAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Attendre que RabbitMQ soit prêt
        loop = asyncio.get_event_loop()
        loop.run_until_complete(wait_for_rabbitmq())
        # Créer les tables de la base de données de test
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Supprimer les tables de la base de données de test
        Base.metadata.drop_all(bind=engine)

    def test_create_commande(self):
        response = self.client.post(
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
        self.client.post(
            "/customers/orders",
            json={
                "clientId": 1,
                "produits": [{"produitId": 1}, {"produitId": 2}]
            },
        )
        self.client.post(
            "/customers/orders",
            json={
                "clientId": 1,
                "produits": [{"produitId": 3}]
            },
        )

        # Maintenant teste la récupération des commandes
        response = self.client.get(f"/customers/1/orders")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["clientId"], 1)
        self.assertEqual(data[1]["clientId"], 1)

        # Teste un client sans commande
        response = self.client.get("/customers/999/orders")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Commandes not found"})

if __name__ == "__main__":
    unittest.main()

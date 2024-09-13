from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from API_Commandes import models, schemas
from API_Commandes.database import engine, get_db
from typing import List
import aio_pika
import os

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Configuration RabbitMQ
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def get_rabbitmq_connection():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection

async def publish_message(queue_name: str, message: str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue.name
        )

# Créer une commande
@app.post("/customers/orders", response_model=schemas.Commande)
async def create_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    db_commande = models.Commande(clientId=commande.clientId)
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    
    for produit in commande.produits:
        db_produit = models.CommandeProduit(commande_id=db_commande.id, produitId=produit.produitId)
        db.add(db_produit)
    
    db.commit()
    db.refresh(db_commande)
    await publish_message("order_created", f"Order created: {db_commande.id}")
    return db_commande

# Récupérer la liste des commandes d'un client
@app.get("/customers/{customer_id}/orders", response_model=List[schemas.Commande])
def read_commande(customer_id: int, db: Session = Depends(get_db)):
    db_commande = db.query(models.Commande).filter(models.Commande.clientId == customer_id).all()
    
    # Vérifier si la liste des commandes est vide
    if not db_commande:
        raise HTTPException(status_code=404, detail="Commandes not found")
    return db_commande

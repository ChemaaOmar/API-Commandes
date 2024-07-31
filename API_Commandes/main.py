from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from API_Commandes import models, schemas
from API_Commandes.database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Créer une commande
@app.post("/customers/orders", response_model=schemas.Commande)
def create_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    db_commande = models.Commande(clientId=commande.clientId)
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    
    for produit in commande.produits:
        db_produit = models.CommandeProduit(commande_id=db_commande.id, produitId=produit.produitId)
        db.add(db_produit)
    
    db.commit()
    db.refresh(db_commande)
    return db_commande

# Récupérer la liste des commandes d'un client
@app.get("/customers/{customer_id}/orders", response_model=schemas.Commande)
def read_commande(customer_id: int, db: Session = Depends(get_db)):
    db_commande = db.query(models.Commande).filter(models.Commande.clientId == customer_id).all()
    if db_commande is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    return db_commande

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    db_commande = db.query(models.Commande).filter(models.Commande.id == customer_id).first()
    if db_commande is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    return db_commande

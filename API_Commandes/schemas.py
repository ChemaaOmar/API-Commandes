from pydantic import BaseModel
from typing import List, Optional

class CommandeProduitBase(BaseModel):
    produitId: int

class CommandeProduitCreate(CommandeProduitBase):
    pass

class CommandeProduit(CommandeProduitBase):
    id: int
    commande_id: int

    class Config:
        orm_mode = True

class CommandeBase(BaseModel):
    clientId: int

class CommandeCreate(CommandeBase):
    produits: List[CommandeProduitCreate] = []

class Commande(CommandeBase):
    id: int
    produits: List[CommandeProduit] = []

    class Config:
        orm_mode = True

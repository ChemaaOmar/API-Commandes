from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Commande(Base):
    __tablename__ = "commandes"
    
    id = Column(Integer, primary_key=True, index=True)
    clientId = Column(Integer, index=True)
    produits = relationship("CommandeProduit", back_populates="commande")

class CommandeProduit(Base):
    __tablename__ = "commande_produits"
    
    id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey('commandes.id'))
    produitId = Column(Integer, index=True)
    commande = relationship("Commande", back_populates="produits")

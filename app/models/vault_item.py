# app/models/vault_item.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- CAMPOS OBLIGATORIOS ---
    # Por defecto, nullable=False, así que no hace falta especificarlo
    username = Column(String, index=True, nullable=False)
    encrypted_password = Column(String, nullable=False)
    url = Column(String, index=True, nullable=False)
    
    # --- CAMPOS OPCIONALES ---
    # Para estos, sí especificamos nullable=True
    notes = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    
    # --- RELACIÓN ---
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="vault_items")
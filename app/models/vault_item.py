from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, index=True, nullable=False)
    encrypted_password = Column(String, nullable=False)
    url = Column(String, index=True, nullable=False)
    
    notes = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="vault_items")
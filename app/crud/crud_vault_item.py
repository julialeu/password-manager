from typing import List
from sqlalchemy.orm import Session
from app.models.vault_item import VaultItem
from app.schemas.vault_item import VaultItemCreate, VaultItemUpdate
from app.core.security import encrypt_data, decrypt_data

def get_vault_item(db: Session, item_id: int, owner_id: int) -> VaultItem | None:
    """Obtiene un item de la bóveda por su ID, asegurando que pertenece al owner_id."""
    return db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.owner_id == owner_id).first()

def get_vault_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[VaultItem]:
    """Obtiene una lista de items de la bóveda para un usuario específico."""
    return db.query(VaultItem).filter(VaultItem.owner_id == owner_id).offset(skip).limit(limit).all()

def create_vault_item(db: Session, item: VaultItemCreate, owner_id: int) -> VaultItem:
    """Crea un nuevo item en la bóveda."""
    encrypted_password = encrypt_data(item.password)
    
    # Convertimos el objeto Pydantic a un diccionario
    item_data = item.model_dump(exclude={"password"})
    
    # Convertimos la URL a string si existe.
    if item_data.get("url"):
        item_data["url"] = str(item_data["url"])

    db_item = VaultItem(
        **item_data, 
        encrypted_password=encrypted_password, 
        owner_id=owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
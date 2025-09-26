from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.vault_item import VaultItem
from app.schemas.vault_item import VaultItemCreate, VaultItemUpdate
from app.core.security import encrypt_data

def get_vault_item(db: Session, item_id: int, owner_id: int) -> VaultItem | None:
    """Retrieves an item from the vault by its ID, ensuring that it belongs to the owner_id."""
    return db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.owner_id == owner_id).first()

def get_vault_items_by_owner(
    db: Session, 
    owner_id: int, 
    skip: int = 0, 
    limit: int = 100,
    search: str | None = None,
    url_filter: str | None = None
) -> List[VaultItem]:
    """
    Get a list of vault items for a specific user,
    with search and filter options.
    """
    query = db.query(VaultItem).filter(VaultItem.owner_id == owner_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                VaultItem.username.ilike(search_term),
                VaultItem.url.ilike(search_term),
                VaultItem.notes.ilike(search_term)
            )
        )
        
    if url_filter:
        url_filter_term = f"%{url_filter}%"
        query = query.filter(VaultItem.url.ilike(url_filter_term))
        
    return query.offset(skip).limit(limit).all()

def create_vault_item(db: Session, item: VaultItemCreate, owner_id: int) -> VaultItem:
    """Crea un nuevo item en la bóveda."""
    encrypted_password = encrypt_data(item.password)
    
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


def update_vault_item(
    db: Session, db_item: VaultItem, item_in: VaultItemUpdate
) -> VaultItem:
    """
    Update an item in the vault.
    """
    update_data = item_in.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        new_encrypted_password = encrypt_data(update_data["password"])
        db_item.encrypted_password = new_encrypted_password
        del update_data["password"]
    else:
        print("A new password has not been provided.")

    for field, value in update_data.items():
        if field == "url" and value is not None:
            value = str(value)
        setattr(db_item, field, value)
        
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        raise e
    
    return db_item

def remove_vault_item(db: Session, item_id: int) -> VaultItem | None:
    """
    Remove an item from the vault.
    """
    db_item = db.query(VaultItem).filter(VaultItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item    
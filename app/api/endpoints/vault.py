# app/api/endpoints/vault.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User as UserModel
from app.schemas.vault_item import VaultItem, VaultItemCreate, VaultItemUpdate, VaultItemWithPassword
from app.crud import crud_vault_item
from app.core.security import decrypt_data

router = APIRouter()

@router.post("/", response_model=VaultItem, status_code=status.HTTP_201_CREATED)
def create_vault_item(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
    item_in: VaultItemCreate
):
    """
    Crea un nuevo item en la bóveda para el usuario actual.
    """
    item = crud_vault_item.create_vault_item(db=db, item=item_in, owner_id=current_user.id)
    return item

@router.get("/", response_model=List[VaultItem])
def read_vault_items(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtiene la lista de items de la bóveda para el usuario actual.
    """
    items = crud_vault_item.get_vault_items_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=VaultItemWithPassword)
def read_vault_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Obtiene los detalles de un item específico de la bóveda, incluyendo la contraseña descifrada.
    """
    item = crud_vault_item.get_vault_item(db, item_id=item_id, owner_id=current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Vault item not found")
    
    # Desciframos la contraseña antes de devolverla
    decrypted_password = decrypt_data(item.encrypted_password)
    
    # Creamos un diccionario con los datos del item y la contraseña descifrada
    item_data = VaultItem.model_validate(item).model_dump()
    item_data["password"] = decrypted_password
    
    return VaultItemWithPassword(**item_data)
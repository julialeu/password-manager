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
    Create a new item in the vault for the current user.
    """
    item = crud_vault_item.create_vault_item(db=db, item=item_in, owner_id=current_user.id)
    return item

@router.get("/", response_model=List[VaultItem])
def read_vault_items(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    url_filter: str | None = None
):
    """
    Gets the list of items in the vault for the current user.
    - `q`: Free text search in username, URL, and notes.
    - `url_filter`: Filters items whose URL contains this text.
    """
    items = crud_vault_item.get_vault_items_by_owner(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        search=q,
        url_filter=url_filter
    )
    return items

@router.get("/{item_id}", response_model=VaultItemWithPassword)
def read_vault_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Obtains the details of a specific item in the vault, including the decrypted password.
    """
    item = crud_vault_item.get_vault_item(db, item_id=item_id, owner_id=current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Vault item not found")

    decrypted_password = decrypt_data(item.encrypted_password)

    item_data = VaultItem.model_validate(item).model_dump()
    item_data["password"] = decrypted_password

    return VaultItemWithPassword(**item_data)

@router.put("/{item_id}", response_model=VaultItem)
def update_vault_item(
    item_id: int,
    item_in: VaultItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Update an item in the vault.
    """
    
    db_item = crud_vault_item.get_vault_item(db, item_id=item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Vault item not found")
    
    item = crud_vault_item.update_vault_item(db=db, db_item=db_item, item_in=item_in)
    return item

@router.delete("/{item_id}", response_model=VaultItem)
def delete_vault_item(
    item_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Remove an item from the vault.
    """
    db_item = crud_vault_item.get_vault_item(db, item_id=item_id, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Vault item not found")

    item = crud_vault_item.remove_vault_item(db=db, item_id=item_id)
    return item
from pydantic import BaseModel, HttpUrl, ConfigDict

class VaultItemBase(BaseModel):
    username: str | None = None
    url: HttpUrl | None = None
    notes: str | None = None
    icon: str | None = None

class VaultItemCreate(VaultItemBase):
    password: str

class VaultItemUpdate(VaultItemBase):
    password: str | None = None

class VaultItemInDBBase(VaultItemBase):
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)

class VaultItem(VaultItemInDBBase):
    pass

# Schema que puede incluir la contraseña descifrada (para el modal con el detalle)
class VaultItemWithPassword(VaultItem):
    password: str
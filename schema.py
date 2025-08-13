from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator


class AddProd(BaseModel):
    title: str
    price: int
    
    
    @field_validator('title', mode="before")
    def valid_title(cls, value):
        if not value:
            raise ValueError("veuillez saisir le titre")
        return value
    
class UpdateProd(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
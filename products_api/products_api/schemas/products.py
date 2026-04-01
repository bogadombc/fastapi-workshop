from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: Decimal
    description: Optional[str] = None


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: Decimal
    description: Optional[str] = None


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None


class ProductListResponseSchema(BaseModel):
    products: List[ProductResponseSchema]
